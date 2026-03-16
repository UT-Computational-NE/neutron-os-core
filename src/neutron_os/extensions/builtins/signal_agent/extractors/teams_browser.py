"""Teams Browser Extractor — fetches meeting transcripts via Playwright.

Uses browser automation to authenticate with your regular Microsoft account
and download meeting transcripts from Teams/OneDrive. No developer API
access or MS Graph credentials required — just your user login.

First run: interactive browser for MFA. Subsequent runs: fully headless
using persisted session cookies.

Usage:
    # First time (opens browser for login)
    neut signal ingest --source teams-browser --headed

    # Subsequent runs (headless, uses saved session)
    neut signal ingest --source teams-browser

    # Fetch last 30 days of transcripts
    neut signal ingest --source teams-browser --days 30

Requires: pip install playwright && playwright install chromium
"""

from __future__ import annotations

import json
import logging
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from neutron_os import REPO_ROOT as _REPO_ROOT

from ..models import Extraction, Signal
from ..registry import register_source, SourceType
from .base import BaseExtractor

logger = logging.getLogger(__name__)

_RUNTIME_DIR = _REPO_ROOT / "runtime"
_SESSION_DIR = _RUNTIME_DIR / "inbox" / "state" / "teams_browser_session"
_RAW_TEAMS_DIR = _RUNTIME_DIR / "inbox" / "raw" / "teams"
_DOWNLOAD_DIR = _RAW_TEAMS_DIR / "transcripts"

# Microsoft 365 URLs
_TEAMS_URL = "https://teams.microsoft.com"
_ONEDRIVE_URL = "https://onedrive.live.com"
_LOGIN_URL = "https://login.microsoftonline.com"

# Selectors (may need updating if Microsoft changes their UI)
_TRANSCRIPTS_URL = (
    "https://teams.microsoft.com/_#/calendarv2"
)


@register_source(
    name="teams_browser",
    description="Teams meeting transcripts via browser automation (no API keys needed)",
    source_type=SourceType.PULL,
    requires_auth=False,  # Uses browser session, not API keys
    file_patterns=["*.vtt", "*.docx"],
    default_poll_interval=3600,  # 1 hour
    icon="🌐",
    category="meetings",
)
class TeamsBrowserExtractor(BaseExtractor):
    """Fetch Teams meeting transcripts using Playwright browser automation.

    Authenticates as the user via their regular Microsoft account.
    Session cookies are persisted so MFA is only needed once.
    """

    @property
    def name(self) -> str:
        return "teams_browser"

    def __init__(
        self,
        session_dir: Optional[Path] = None,
        download_dir: Optional[Path] = None,
        headless: bool = True,
        days: int = 7,
    ):
        self.session_dir = session_dir or _SESSION_DIR
        self.download_dir = download_dir or _DOWNLOAD_DIR
        self.headless = headless
        self.days = days

    @staticmethod
    def is_available() -> bool:
        """Check if Playwright is installed."""
        try:
            import playwright  # noqa: F401
            return True
        except ImportError:
            return False

    def can_handle(self, path: Path) -> bool:
        return False  # This extractor fetches, doesn't process local files

    def ensure_playwright(self) -> None:
        """Verify Playwright and Chromium are installed."""
        try:
            from playwright.sync_api import sync_playwright  # noqa: F401
        except ImportError:
            raise RuntimeError(
                "Playwright not installed. Run:\n"
                "  pip install playwright && playwright install chromium"
            )

    def has_session(self) -> bool:
        """Check if a saved browser session exists."""
        return (self.session_dir / "state.json").exists()

    def fetch_transcripts(
        self,
        days: Optional[int] = None,
        headless: Optional[bool] = None,
    ) -> list[Path]:
        """Fetch meeting transcripts from Teams.

        Args:
            days: How many days back to fetch (default: self.days)
            headless: Override headless mode (default: self.headless,
                      but forced to False if no session exists for first login)

        Returns:
            List of paths to downloaded transcript files.
        """
        self.ensure_playwright()
        from playwright.sync_api import sync_playwright

        days = days or self.days
        if headless is None:
            headless = self.headless
            # Force headed mode for first login (MFA)
            if not self.has_session() and headless:
                logger.info(
                    "No saved session — launching browser for initial login. "
                    "Use --headed flag to see the browser window."
                )
                headless = False

        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.download_dir.mkdir(parents=True, exist_ok=True)

        downloaded: list[Path] = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)

            # Load saved session or start fresh
            context = browser.new_context(
                storage_state=str(self.session_dir / "state.json")
                if self.has_session()
                else None,
                accept_downloads=True,
            )

            page = context.new_page()

            try:
                # Navigate to Teams
                page.goto(_TEAMS_URL, wait_until="domcontentloaded", timeout=30000)

                # Check if we need to log in
                if self._needs_login(page):
                    self._do_login(page, headless)

                # Save session state after successful auth
                context.storage_state(path=str(self.session_dir / "state.json"))

                # Navigate to recent meetings and download transcripts
                downloaded = self._fetch_recent_transcripts(page, context, days)

                # Save session state again (cookies may have refreshed)
                context.storage_state(path=str(self.session_dir / "state.json"))

            except Exception as e:
                logger.error("Teams browser fetch failed: %s", e)
                # Save session anyway so partial auth isn't lost
                try:
                    context.storage_state(path=str(self.session_dir / "state.json"))
                except Exception:
                    pass
                raise
            finally:
                context.close()
                browser.close()

        return downloaded

    def _needs_login(self, page) -> bool:
        """Check if the page redirected to Microsoft login."""
        url = page.url
        return (
            "login.microsoftonline.com" in url
            or "login.live.com" in url
            or "login.microsoft.com" in url
        )

    def _do_login(self, page, headless: bool) -> None:
        """Handle Microsoft login flow.

        For headed mode: wait for the user to complete login + MFA.
        For headless mode: this shouldn't be called (session should exist).
        """
        if headless:
            raise RuntimeError(
                "Login required but running headless. "
                "Run once with --headed to authenticate:\n"
                "  neut signal ingest --source teams-browser --headed"
            )

        print("\n  Microsoft login required.")
        print("  Complete the login in the browser window (including MFA).")
        print("  Waiting for authentication...\n")

        # Wait for redirect back to Teams (up to 5 minutes for MFA)
        try:
            page.wait_for_url(
                re.compile(r"teams\.microsoft\.com"),
                timeout=300_000,
            )
            print("  ✓ Login successful — session saved for future headless use.\n")
        except Exception:
            raise RuntimeError(
                "Login timed out. Complete the login within 5 minutes."
            )

    def _fetch_recent_transcripts(
        self, page, context, days: int,
    ) -> list[Path]:
        """Navigate to recent meetings and download available transcripts."""
        downloaded: list[Path] = []
        since = datetime.now(timezone.utc) - timedelta(days=days)

        # Navigate to Teams calendar view
        try:
            page.goto(
                "https://teams.microsoft.com/_#/calendarv2",
                wait_until="domcontentloaded",
                timeout=30000,
            )
            page.wait_for_timeout(3000)  # Let calendar load
        except Exception as e:
            logger.warning("Could not load Teams calendar: %s", e)
            # Try OneDrive recordings folder as fallback
            return self._fetch_from_onedrive(page, context, days)

        # Look for meetings with transcripts
        # The Teams calendar shows recent meetings; each may have a transcript
        meeting_elements = page.query_selector_all(
            "[data-tid='calendar-event'], .calendar-event, [role='listitem']"
        )

        if not meeting_elements:
            logger.info("No meeting elements found on calendar. Trying OneDrive fallback.")
            return self._fetch_from_onedrive(page, context, days)

        for meeting_el in meeting_elements[:20]:  # Cap at 20 most recent
            try:
                meeting_el.click()
                page.wait_for_timeout(1000)

                # Look for transcript/recording tab or download link
                transcript_link = page.query_selector(
                    "[data-tid='transcript-tab'], "
                    "button:has-text('Transcript'), "
                    "a:has-text('transcript'), "
                    "a:has-text('recording')"
                )

                if transcript_link:
                    transcript_link.click()
                    page.wait_for_timeout(2000)

                    # Try to download the transcript
                    download_link = page.query_selector(
                        "a:has-text('Download'), "
                        "button:has-text('Download'), "
                        "[data-tid='download-transcript']"
                    )

                    if download_link:
                        with page.expect_download(timeout=15000) as download_info:
                            download_link.click()
                        download = download_info.value
                        dest = self.download_dir / download.suggested_filename
                        download.save_as(str(dest))
                        downloaded.append(dest)
                        logger.info("Downloaded transcript: %s", dest.name)

                # Close the meeting detail
                close_btn = page.query_selector(
                    "button[aria-label='Close'], "
                    "button:has-text('Close'), "
                    "[data-tid='close-button']"
                )
                if close_btn:
                    close_btn.click()
                    page.wait_for_timeout(500)

            except Exception as e:
                logger.debug("Skipping meeting element: %s", e)
                continue

        return downloaded

    def _fetch_from_onedrive(
        self, page, context, days: int,
    ) -> list[Path]:
        """Fallback: fetch transcripts from OneDrive Recordings folder.

        Teams stores meeting recordings and transcripts in the user's
        OneDrive under 'Recordings' folder.
        """
        downloaded: list[Path] = []

        try:
            # Navigate to OneDrive Recordings folder
            page.goto(
                "https://onedrive.live.com/?view=folder",
                wait_until="domcontentloaded",
                timeout=30000,
            )
            page.wait_for_timeout(3000)

            # Try to find Recordings folder
            recordings_link = page.query_selector(
                "a:has-text('Recordings'), "
                "[data-automationid='FieldRenderer-name']:has-text('Recordings')"
            )

            if recordings_link:
                recordings_link.click()
                page.wait_for_timeout(2000)

                # Find transcript files (.vtt, .docx)
                file_links = page.query_selector_all(
                    "[data-automationid='FieldRenderer-name']"
                )

                for link in file_links:
                    name = link.inner_text().strip()
                    if any(name.endswith(ext) for ext in (".vtt", ".docx", ".txt")):
                        # Right-click → Download
                        link.click(button="right")
                        page.wait_for_timeout(500)

                        download_option = page.query_selector(
                            "button:has-text('Download'), "
                            "[data-automationid='downloadCommand']"
                        )

                        if download_option:
                            with page.expect_download(timeout=15000) as download_info:
                                download_option.click()
                            download = download_info.value
                            dest = self.download_dir / download.suggested_filename
                            download.save_as(str(dest))
                            downloaded.append(dest)
                            logger.info("Downloaded from OneDrive: %s", dest.name)

        except Exception as e:
            logger.warning("OneDrive fallback failed: %s", e)

        return downloaded

    def extract(self, source_path: Path, **kwargs) -> Extraction:
        """Fetch transcripts from Teams and return extraction results.

        Unlike other extractors that process local files, this one
        fetches from the network first, then delegates to the
        TranscriptExtractor for signal extraction.
        """
        errors: list[str] = []
        signals: list[Signal] = []

        try:
            downloaded = self.fetch_transcripts(
                days=kwargs.get("days", self.days),
                headless=kwargs.get("headless", self.headless),
            )
        except Exception as e:
            return Extraction(
                extractor=self.name,
                source_file="teams-browser",
                errors=[str(e)],
            )

        if not downloaded:
            return Extraction(
                extractor=self.name,
                source_file="teams-browser",
                signals=[],
                errors=["No transcripts found in the specified time window."],
            )

        # Process each downloaded file through the TranscriptExtractor
        from .transcript import TranscriptExtractor
        transcript_extractor = TranscriptExtractor()

        for path in downloaded:
            try:
                result = transcript_extractor.extract(path)
                signals.extend(result.signals)
                errors.extend(result.errors)
            except Exception as e:
                errors.append(f"Failed to process {path.name}: {e}")

        return Extraction(
            extractor=self.name,
            source_file="teams-browser",
            signals=signals,
            errors=errors,
        )

    def clear_session(self) -> None:
        """Clear saved browser session (forces re-login on next run)."""
        state_file = self.session_dir / "state.json"
        if state_file.exists():
            state_file.unlink()
            logger.info("Browser session cleared. Next run will require login.")
