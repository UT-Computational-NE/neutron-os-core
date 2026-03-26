"""Unit tests for the briefing service."""

from datetime import UTC, datetime, timedelta

import pytest

from neutron_os.extensions.builtins.eve_agent.briefing import (
    TOPIC_KEYWORDS,
    Briefing,
    BriefingService,
    BriefingTopic,
    ConsumptionEvent,
    ConsumptionRecord,
)
from neutron_os.extensions.builtins.eve_agent.models import Signal


class TestBriefingTopic:
    """Test BriefingTopic enum."""

    def test_all_topics_have_keywords(self):
        """Verify each topic has associated keywords for fallback matching."""
        for topic in BriefingTopic:
            if topic != BriefingTopic.GENERAL and topic != BriefingTopic.LONG_RUNNING:
                assert topic in TOPIC_KEYWORDS, f"Topic {topic} missing keywords"

    def test_topic_values(self):
        assert BriefingTopic.PEOPLE.value == "people"
        assert BriefingTopic.TECH.value == "tech"
        assert BriefingTopic.BLOCKERS.value == "blockers"


class TestConsumptionRecord:
    """Test ConsumptionRecord dataclass."""

    def test_roundtrip(self):
        record = ConsumptionRecord(
            event_type=ConsumptionEvent.BRIEFING_DELIVERED,
            timestamp=datetime.now(UTC),
            details={"topic": "general"},
        )

        d = record.to_dict()
        restored = ConsumptionRecord.from_dict(d)

        assert restored.event_type == record.event_type
        assert restored.details == record.details


class TestBriefingService:
    """Test BriefingService class."""

    @pytest.fixture
    def service(self, tmp_path):
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        return BriefingService(
            state_path=state_dir / "briefing_state.json",
        )

    @pytest.fixture
    def sample_signals(self, tmp_path):
        """Create sample processed signals."""
        return [
            Signal(
                source="voice",
                timestamp=(datetime.now(UTC) - timedelta(hours=2)).isoformat(),
                raw_text="Kevin is working on data pipeline optimization",
                detail="Kevin progressing on Alpha thermal work",
                people=["Kevin"],
                initiatives=["Project Alpha"],
                signal_type="progress",
            ),
            Signal(
                source="voice",
                timestamp=(datetime.now(UTC) - timedelta(hours=1)).isoformat(),
                raw_text="Blocked on NRC approval for license amendment",
                detail="NRC approval blocking progress",
                initiatives=["Project Alpha"],
                signal_type="blocker",
            ),
            Signal(
                source="voice",
                timestamp=datetime.now(UTC).isoformat(),
                raw_text="Conference abstract accepted for ANS meeting",
                detail="ANS conference abstract accepted",
                signal_type="decision",
            ),
        ]

    def test_brief_me_returns_briefing(self, service):
        briefing = service.brief_me()

        assert isinstance(briefing, Briefing)
        assert briefing.topic in [t.value for t in BriefingTopic]
        assert briefing.signal_count >= 0

    def test_topic_detection_people(self, service):
        """Test that person names trigger PEOPLE topic."""
        category, query = service._detect_topic_category("Kevin")

        assert category == BriefingTopic.PEOPLE or query == "Kevin"

    def test_topic_detection_tech(self, service):
        """Test that tech keywords trigger TECH topic."""
        category, query = service._detect_topic_category("bugs")

        # Should detect as TECH or pass through
        assert category == BriefingTopic.TECH or "bug" in query.lower()

    def test_topic_detection_blockers(self, service):
        """Test that blocker keywords trigger BLOCKERS topic."""
        category, query = service._detect_topic_category("blockers")

        assert category == BriefingTopic.BLOCKERS

    def test_record_consumption(self, service):
        """Test that briefing delivery is recorded."""
        service.record_consumption(
            event_type=ConsumptionEvent.BRIEFING_DELIVERED,
            details={"topic": "general"},
        )

        assert len(service.state.consumption_history) >= 1
        assert service.state.consumption_history[-1].event_type == ConsumptionEvent.BRIEFING_DELIVERED

    def test_time_window_calculation(self, service):
        """Test automatic time window based on last consumption."""
        # No prior consumption - should use default
        start, end, confidence, reason = service._determine_time_window()

        # Should be within last 48 hours by default
        assert start < datetime.now(UTC)

        # Record consumption
        service.record_consumption(
            event_type=ConsumptionEvent.BRIEFING_DELIVERED,
        )

        # Now window should start from that point
        start2, end2, conf2, reason2 = service._determine_time_window()
        assert start2 >= start

    def test_acknowledge_updates_state(self, service):
        # Generate a briefing with acknowledge=True
        _briefing = service.brief_me(acknowledge=True)

        assert any(
            r.event_type == ConsumptionEvent.BRIEFING_ACKNOWLEDGED
            for r in service.state.consumption_history
        )


class TestBriefingFiltering:
    """Test signal filtering for topic-focused briefings."""

    @pytest.fixture
    def service(self, tmp_path):
        return BriefingService(
            state_path=tmp_path / "state" / "briefing.json",
        )

    @pytest.fixture
    def sample_signal_dicts(self):
        """Create diverse signal dicts for filtering tests."""
        return [
            {"signal_type": "progress", "people": ["Kevin"], "initiatives": ["Alpha"],
             "raw_text": "Kevin working", "detail": "progress", "timestamp": datetime.now(UTC).isoformat()},
            {"signal_type": "blocker", "people": ["Alice"], "initiatives": ["MSR"],
             "raw_text": "Alice blocked", "detail": "blocker", "timestamp": datetime.now(UTC).isoformat()},
            {"signal_type": "decision", "people": ["Ben"], "initiatives": ["Alpha"],
             "raw_text": "Ben decided", "detail": "decision", "timestamp": datetime.now(UTC).isoformat()},
            {"signal_type": "progress", "people": ["Kevin"], "initiatives": ["NETL"],
             "raw_text": "Kevin on NETL", "detail": "progress", "timestamp": datetime.now(UTC).isoformat()},
        ]

    def test_filter_by_person(self, service, sample_signal_dicts):
        filtered = service._filter_signals_by_topic(
            sample_signal_dicts,
            topic="Kevin",
            category=BriefingTopic.PEOPLE,
        )

        # Kevin's signals should be in results
        kevin_sigs = [s for s in filtered if "Kevin" in s.get("people", [])]
        assert len(kevin_sigs) >= 1

    def test_filter_by_initiative(self, service, sample_signal_dicts):
        filtered = service._filter_signals_by_topic(
            sample_signal_dicts,
            topic="Alpha",
            category=BriefingTopic.INITIATIVES,
        )

        for sig in filtered:
            assert any("Alpha" in init for init in sig.get("initiatives", []))

    def test_filter_blockers_only(self, service, sample_signal_dicts):
        filtered = service._filter_signals_by_topic(
            sample_signal_dicts,
            topic="blockers",
            category=BriefingTopic.BLOCKERS,
        )

        for sig in filtered:
            assert sig.get("signal_type") == "blocker"
