"""Post-setup hooks and lifecycle management for neut_agent connections.

Called by neut connect when a connection declares post_setup_module
pointing here. Keeps tool-specific setup logic in the owning extension.
"""

from __future__ import annotations

import logging
import platform
import shutil
import subprocess
import time
import urllib.request

log = logging.getLogger(__name__)


def setup_ollama() -> int:
    """Post-install hook for Ollama: register as service + pull routing model.

    Called by `neut connect ollama` after installation. Ensures Ollama
    runs persistently (survives reboots) and the routing model is pulled.
    The user should never think about Ollama lifecycle after this.
    """
    from neutron_os.extensions.builtins.settings.store import SettingsStore

    settings = SettingsStore()
    model = settings.get("routing.ollama_model", "llama3.2:1b")

    # Start as a persistent service (not a raw subprocess)
    if not _is_ollama_serving():
        _start_ollama_service()
        # Wait for it to come up
        for _ in range(8):
            time.sleep(1)
            if _is_ollama_serving():
                print("  \u2713 Ollama running (managed service)")
                break
        else:
            print("  \u26a0 Ollama service didn't start")
            print("    Check with: brew services info ollama")
            return 1
    else:
        print("  \u2713 Ollama already running")

    # Pull routing model if needed
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=10,
        )
        if model in result.stdout:
            print(f"  \u2713 Model {model} ready")
            print()
            return 0
    except Exception:
        pass

    print(f"  Pulling routing model ({model})...")
    try:
        subprocess.run(
            ["ollama", "pull", model],
            check=True, timeout=300,
        )
        print(f"  \u2713 Model {model} ready")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print(f"  \u2717 Pull failed \u2014 try manually: ollama pull {model}")
        return 1

    print()
    return 0


def ensure_ollama_running() -> bool:
    """Silently ensure Ollama is serving. Called by the router before inference.

    Returns True if Ollama is available, False if not installed or won't start.
    Never prompts, never prints — this is a background operation.
    """
    if not shutil.which("ollama"):
        return False

    if _is_ollama_serving():
        return True

    # Try to start it silently
    _start_ollama_service(silent=True)

    # Wait briefly
    for _ in range(5):
        time.sleep(0.5)
        if _is_ollama_serving():
            log.info("Ollama auto-started")
            return True

    log.debug("Ollama auto-start failed")
    return False


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _is_ollama_serving() -> bool:
    """Check if Ollama API is responding."""
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=1)
        return True
    except Exception:
        return False


def _start_ollama_service(silent: bool = False) -> None:
    """Start Ollama as a managed service (persists across reboots)."""
    if platform.system() == "Darwin" and shutil.which("brew"):
        try:
            subprocess.run(
                ["brew", "services", "start", "ollama"],
                capture_output=True, timeout=15,
            )
            if not silent:
                print("  Starting via brew services...")
            return
        except Exception:
            pass

    # Fallback: raw background process (Linux, or brew not available)
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if not silent:
            print("  Starting ollama serve...")
    except Exception:
        pass
