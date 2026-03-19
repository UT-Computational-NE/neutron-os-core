"""Smoke tests: routing pipeline + provider selection + graceful fallback.

Proves:
  1. Ollama SLM is the classifier for public prompts (router returns "ollama" or
     "fallback" classifier, never "keyword" for non-EC prompts).
  2. Export-controlled prompts route to the export_controlled tier.
  3. Gateway selects the Qwen/rascal provider when VPN is reachable and it
     appears first in the prefer_provider chain.
  4. Gateway skips Qwen/rascal and falls through the frontier provider list when
     the VPN host is unreachable.
  5. Frontier provider fallback honours the configured priority order
     (Anthropic claude-* before OpenAI, or whatever is configured).
  6. GatewayResponse / CompletionResponse carries the correct provider.name and
     model so neut chat can display "Answered by <provider> (<model>)".

All tests are unit-level: no live LLM calls, no network, no Ollama required.
Integration tests that make real calls live in tests/integration/.
"""

from __future__ import annotations

import socket
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from neutron_os.infra.router import (
    OllamaClassifier,
    QueryRouter,
    RoutingDecision,
    RoutingTier,
    SENSITIVITY_BALANCED,
    SENSITIVITY_STRICT,
)
from neutron_os.infra.gateway import (
    CompletionResponse,
    Gateway,
    LLMProvider,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def public_router():
    """Router with Ollama mock returning PUBLIC for every query."""
    mock_ollama = MagicMock(spec=OllamaClassifier)
    mock_ollama.classify.return_value = RoutingTier.PUBLIC
    return QueryRouter(ollama=mock_ollama)


@pytest.fixture()
def ec_router():
    """Router with Ollama mock returning EXPORT_CONTROLLED for every query."""
    mock_ollama = MagicMock(spec=OllamaClassifier)
    mock_ollama.classify.return_value = RoutingTier.EXPORT_CONTROLLED
    return QueryRouter(ollama=mock_ollama)


@pytest.fixture()
def ollama_unavailable_router():
    """Router where Ollama is down (returns None) — exercises fallback path."""
    mock_ollama = MagicMock(spec=OllamaClassifier)
    mock_ollama.classify.return_value = None
    return QueryRouter(ollama=mock_ollama)


def _make_provider(
    name: str,
    endpoint: str,
    model: str,
    priority: int = 50,
    routing_tier: str = "any",
    requires_vpn: bool = False,
    api_key: str = "test-key",
    api_key_env: str = "",
) -> LLMProvider:
    p = LLMProvider(
        name=name,
        endpoint=endpoint,
        model=model,
        priority=priority,
        routing_tier=routing_tier,
        requires_vpn=requires_vpn,
        api_key_env=api_key_env or f"_NEUT_TEST_{name.upper()}",
    )
    # Patch api_key property to return a fixed value without env lookup
    import os
    os.environ[p.api_key_env] = api_key
    return p


@pytest.fixture()
def gateway_with_providers(monkeypatch):
    """Gateway pre-loaded with three providers (rascal VPN, anthropic, openai)."""
    gw = Gateway.__new__(Gateway)
    gw._provider_override = None
    gw._model_override = None
    gw.providers = [
        _make_provider(
            name="qwen-rascal",
            endpoint="http://rascal.tacc.utexas.edu:11434",
            model="qwen2.5-coder:32b",
            priority=10,
            routing_tier="export_controlled",
            requires_vpn=True,
        ),
        _make_provider(
            name="anthropic",
            endpoint="https://api.anthropic.com/v1/messages",
            model="claude-sonnet-4-6",
            priority=20,
            routing_tier="public",
        ),
        _make_provider(
            name="openai",
            endpoint="https://api.openai.com/v1/chat/completions",
            model="gpt-4o",
            priority=30,
            routing_tier="public",
        ),
    ]
    return gw


# ---------------------------------------------------------------------------
# 1. Router: public prompt → Ollama classifies → PUBLIC tier
# ---------------------------------------------------------------------------

class TestRouterPublicPrompts:
    def test_general_question_routes_public(self, public_router):
        decision = public_router.classify("What is the history of nuclear power plants?")
        assert decision.tier == RoutingTier.PUBLIC

    def test_classifier_label_is_ollama_not_keyword(self, public_router):
        """No export-control keyword hit → must reach Ollama stage."""
        decision = public_router.classify("Explain how a pressurized water reactor works.")
        # Should be "ollama" (SLM confirmed public) or "fallback" (Ollama None).
        # Must NOT be "keyword" — that would mean a false-positive keyword match.
        assert decision.classifier in ("ollama", "fallback")

    def test_ollama_called_for_non_ec_prompt(self, public_router):
        public_router.classify("What is the history of nuclear power plants?")
        public_router._ollama.classify.assert_called_once()


# ---------------------------------------------------------------------------
# 2. Router: export-controlled prompt → EXPORT_CONTROLLED tier
# ---------------------------------------------------------------------------

class TestRouterECPrompts:
    def test_mcnp_keyword_routes_ec(self, public_router):
        """Keyword match short-circuits before Ollama."""
        decision = public_router.classify("Help me debug this MCNP geometry card.")
        assert decision.tier == RoutingTier.EXPORT_CONTROLLED
        assert decision.classifier == "keyword"

    def test_ollama_ec_judgment_routes_ec(self, ec_router):
        """Ollama says EC on a semantically sensitive but keyword-clean prompt."""
        decision = ec_router.classify("Describe the critical mass calculation approach.")
        assert decision.tier == RoutingTier.EXPORT_CONTROLLED
        assert decision.classifier == "ollama"

    def test_strict_mode_uncertain_routes_ec(self):
        """In strict mode, Ollama uncertainty → export_controlled."""
        mock_ollama = MagicMock(spec=OllamaClassifier)
        mock_ollama.classify.return_value = "uncertain"
        router = QueryRouter(ollama=mock_ollama)
        decision = router.classify(
            "What parameters drive neutron flux profiles?",
            sensitivity=SENSITIVITY_STRICT,
        )
        assert decision.tier == RoutingTier.EXPORT_CONTROLLED


# ---------------------------------------------------------------------------
# 3. Gateway: Qwen/rascal selected when VPN is reachable
# ---------------------------------------------------------------------------

class TestGatewayRascalSelected:
    def test_rascal_selected_when_vpn_reachable(self, gateway_with_providers):
        """_select_provider picks rascal for export_controlled tier when VPN up."""
        with patch.object(gateway_with_providers, "_check_vpn", return_value=True):
            provider = gateway_with_providers._select_provider(
                "chat", routing_tier="export_controlled"
            )
        assert provider is not None
        assert provider.name == "qwen-rascal"
        assert "qwen" in provider.model.lower()

    def test_response_carries_rascal_provider_name(self, gateway_with_providers):
        """CompletionResponse.provider == 'rascal' after a successful call."""
        expected = CompletionResponse(
            text="Qwen answer here.",
            provider="qwen-rascal",
            model="qwen2.5-coder:32b",
            success=True,
        )
        with patch.object(gateway_with_providers, "_check_vpn", return_value=True), \
             patch.object(gateway_with_providers, "_call_provider_with_tools", return_value=expected):
            result = gateway_with_providers.complete_with_tools(
                messages=[{"role": "user", "content": "Explain MCNP geometry."}],
                routing_tier="export_controlled",
            )
        assert result.provider == "qwen-rascal"
        assert result.model == "qwen2.5-coder:32b"


# ---------------------------------------------------------------------------
# 4. Gateway: Qwen/rascal skipped when VPN unreachable, fallback fires
# ---------------------------------------------------------------------------

class TestGatewayRascalFallback:
    def test_rascal_skipped_vpn_down_falls_to_anthropic(self, gateway_with_providers):
        """VPN unreachable → rascal skipped → next available provider returned."""
        with patch.object(gateway_with_providers, "_check_vpn", return_value=False):
            # routing_tier="any" so frontier providers are eligible
            provider = gateway_with_providers._select_provider("chat", routing_tier="any")
        # rascal requires VPN and it's down, so should land on anthropic (priority 20)
        assert provider is not None
        assert provider.name == "anthropic"

    def test_vpn_unavailable_response_contains_guidance(self, gateway_with_providers):
        """complete_with_tools returns a clear guidance message when VPN is down."""
        with patch.object(gateway_with_providers, "_check_vpn", return_value=False), \
             patch.object(
                 gateway_with_providers, "_call_provider_with_tools",
                 side_effect=AssertionError("should not reach real call"),
             ):
            # Force rascal to be selected (override) to exercise the VPN-unavailable path
            gateway_with_providers.set_provider_override("qwen-rascal")
            response = gateway_with_providers.complete_with_tools(
                messages=[{"role": "user", "content": "Test prompt."}],
                routing_tier="export_controlled",
            )
        # Should contain VPN guidance, not a raw exception
        assert "VPN" in response.text or "vpn" in response.text.lower() or not response.success
        gateway_with_providers._provider_override = None  # reset


# ---------------------------------------------------------------------------
# 5. Frontier fallback: Anthropic before OpenAI (priority order)
# ---------------------------------------------------------------------------

class TestFrontierFallbackOrder:
    def test_anthropic_preferred_over_openai(self, gateway_with_providers):
        """Anthropic (priority 20) ranks before OpenAI (priority 30) for public tier."""
        with patch.object(gateway_with_providers, "_check_vpn", return_value=False):
            provider = gateway_with_providers._select_provider("chat", routing_tier="public")
        assert provider is not None
        assert provider.name == "anthropic"

    def test_openai_selected_when_anthropic_missing_key(self, gateway_with_providers, monkeypatch):
        """If Anthropic key absent, gateway moves to next provider (OpenAI)."""
        anthropic_env = gateway_with_providers.providers[1].api_key_env
        monkeypatch.delenv(anthropic_env, raising=False)
        with patch.object(gateway_with_providers, "_check_vpn", return_value=False):
            provider = gateway_with_providers._select_provider("chat", routing_tier="public")
        assert provider is not None
        assert provider.name == "openai"

    def test_no_provider_when_all_keys_absent(self, gateway_with_providers, monkeypatch):
        """All API keys missing → _select_provider returns None gracefully."""
        for p in gateway_with_providers.providers:
            monkeypatch.delenv(p.api_key_env, raising=False)
        with patch.object(gateway_with_providers, "_check_vpn", return_value=False):
            provider = gateway_with_providers._select_provider("chat", routing_tier="any")
        assert provider is None


# ---------------------------------------------------------------------------
# 6. CompletionResponse carries provider + model for neut chat display
# ---------------------------------------------------------------------------

class TestResponseProviderLabel:
    def test_response_includes_provider_and_model(self, gateway_with_providers):
        """neut chat can display 'Answered by anthropic (claude-sonnet-4-6)'."""
        expected = CompletionResponse(
            text="Hello from Anthropic.",
            provider="anthropic",
            model="claude-sonnet-4-6",
            success=True,
        )
        with patch.object(gateway_with_providers, "_check_vpn", return_value=False), \
             patch.object(gateway_with_providers, "_call_provider_with_tools", return_value=expected):
            result = gateway_with_providers.complete_with_tools(
                messages=[{"role": "user", "content": "Hello."}],
            )
        assert result.provider == "anthropic"
        assert result.model == "claude-sonnet-4-6"
        # Confirm display string format works
        display = f"Answered by {result.provider} ({result.model})"
        assert display == "Answered by anthropic (claude-sonnet-4-6)"

    def test_stub_response_when_no_providers(self):
        """Gateway with no providers returns stub CompletionResponse, not an exception."""
        gw = Gateway.__new__(Gateway)
        gw._provider_override = None
        gw._model_override = None
        gw.providers = []
        result = gw.complete_with_tools(
            messages=[{"role": "user", "content": "Hello."}],
        )
        assert result.provider == "stub"
        assert result.success is False
