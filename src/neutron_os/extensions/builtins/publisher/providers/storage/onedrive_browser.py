"""OneDrive Browser Storage — uploads .docx files via Playwright.

No MS Graph API credentials needed. Uses the same browser session model
as the Teams browser extractor: first run opens a browser for login,
subsequent runs are fully headless.

Session cookies stored at ~/.neut/credentials/onedrive/ (user-scoped).

Usage:
    # First time (opens browser for login)
    neut pub push --storage onedrive-browser --headed docs/my-doc.docx

    # Subsequent runs (headless)
    neut pub push --storage onedrive-browser docs/my-doc.docx

    # Bulk push all generated .docx files
    neut pub push --storage onedrive-browser --all

Requires: pip install playwright && playwright install chromium
"""

from __future__ import annotations

import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Optional

from ...factory import PublisherFactory
from ..base import StorageProvider, UploadResult, StorageEntry

logger = logging.getLogger(__name__)

_SESSION_DIR = Path.home() / ".neut" / "credentials" / "onedrive"

# Default SharePoint/OneDrive folder for published docs
_DEFAULT_FOLDER = "/Documents/NeutronOS/"
_DEFAULT_DRAFT_FOLDER = "/Documents/NeutronOS/Drafts/"


class OneDriveBrowserStorageProvider(StorageProvider):
    """Microsoft OneDrive/SharePoint storage via Playwright browser automation.

    Authenticates as the user via their regular Microsoft account.
    No developer API credentials needed.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        config = config or {}
        self.session_dir = Path(
            config.get("session_dir")
            or os.environ.get("NEUT_ONEDRIVE_SESSION_DIR")
            or str(_SESSION_DIR)
        )
        self.target_folder = config.get("folder", _DEFAULT_FOLDER)
        self.draft_folder = config.get("draft_folder", _DEFAULT_DRAFT_FOLDER)
        self.headless = config.get("headless", True)
        self.site_url = config.get(
            "site_url",
            os.environ.get("NEUT_SHAREPOINT_URL", ""),
        )

    @staticmethod
    def _ensure_playwright():
        try:
            from playwright.sync_api import sync_playwright  # noqa: F401
        except ImportError:
            raise RuntimeError(
                "Playwright not installed. Run:\n"
                "  pip install playwright && playwright install chromium"
            )

    def has_session(self) -> bool:
        return (self.session_dir / "state.json").exists()

    def is_available(self) -> bool:
        try:
            import playwright  # noqa: F401
            return True
        except ImportError:
            return False

    def upload(
        self,
        local_path: Path,
        remote_name: str | None = None,
        *,
        draft: bool = False,
        headed: bool = False,
    ) -> UploadResult:
        """Upload a file to OneDrive/SharePoint via browser.

        Args:
            local_path: Path to the local .docx file
            remote_name: Filename on OneDrive (defaults to local filename)
            draft: If True, upload to draft folder
            headed: If True, show browser (for first-time login)

        Returns:
            UploadResult with URL and metadata
        """
        self._ensure_playwright()
        from playwright.sync_api import sync_playwright

        if not local_path.exists():
            return UploadResult(
                success=False,
                url="",
                error=f"File not found: {local_path}",
            )

        remote_name = remote_name or local_path.name
        target = self.draft_folder if draft else self.target_folder
        headless = not headed and self.headless

        # Force headed for first login
        if not self.has_session() and headless:
            headless = False
            logger.info("No saved session — launching browser for login.")

        self.session_dir.mkdir(parents=True, exist_ok=True)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                storage_state=str(self.session_dir / "state.json")
                if self.has_session()
                else None,
            )
            page = context.new_page()

            try:
                result = self._upload_to_onedrive(
                    page, context, local_path, remote_name, target,
                )

                # Save session
                context.storage_state(path=str(self.session_dir / "state.json"))
                os.chmod(str(self.session_dir / "state.json"), 0o600)

                return result

            except Exception as e:
                # Save session even on failure
                try:
                    context.storage_state(path=str(self.session_dir / "state.json"))
                    os.chmod(str(self.session_dir / "state.json"), 0o600)
                except Exception:
                    pass
                return UploadResult(
                    success=False,
                    url="",
                    error=str(e),
                )
            finally:
                context.close()
                browser.close()

    def upload_batch(
        self,
        files: list[Path],
        *,
        draft: bool = False,
        headed: bool = False,
    ) -> list[UploadResult]:
        """Upload multiple files in a single browser session.

        More efficient than calling upload() per file — reuses the same
        browser context and authentication.
        """
        self._ensure_playwright()
        from playwright.sync_api import sync_playwright

        headless = not headed and self.headless
        if not self.has_session() and headless:
            headless = False

        self.session_dir.mkdir(parents=True, exist_ok=True)
        target = self.draft_folder if draft else self.target_folder
        results: list[UploadResult] = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                storage_state=str(self.session_dir / "state.json")
                if self.has_session()
                else None,
            )
            page = context.new_page()

            try:
                for local_path in files:
                    if not local_path.exists():
                        results.append(UploadResult(
                            success=False, url="",
                            error=f"File not found: {local_path}",
                        ))
                        continue

                    result = self._upload_to_onedrive(
                        page, context, local_path, local_path.name, target,
                    )
                    results.append(result)
                    logger.info(
                        "%s %s",
                        "✓" if result.success else "✗",
                        local_path.name,
                    )

                context.storage_state(path=str(self.session_dir / "state.json"))
                os.chmod(str(self.session_dir / "state.json"), 0o600)

            except Exception as e:
                try:
                    context.storage_state(path=str(self.session_dir / "state.json"))
                    os.chmod(str(self.session_dir / "state.json"), 0o600)
                except Exception:
                    pass
                # Mark remaining files as failed
                while len(results) < len(files):
                    results.append(UploadResult(
                        success=False, url="",
                        error=f"Session error: {e}",
                    ))
            finally:
                context.close()
                browser.close()

        return results

    def _resolve_onedrive_url(self) -> str:
        """Resolve the correct OneDrive/SharePoint URL based on user org."""
        if self.site_url:
            return self.site_url

        # Check if user has an org configured
        try:
            from neutron_os.extensions.builtins.settings.store import SettingsStore
            store = SettingsStore()
            org = store.get("user.org", "")
            email = store.get("user.email", "")

            if org:
                # Org OneDrive: https://{org_domain}-my.sharepoint.com/
                org_domain = org.replace(".", "").replace("edu", "")
                # Common patterns: utexas.edu → utexas-my.sharepoint.com
                # But actual domain varies — try the email-based pattern
                if email:
                    # bbooth@utexas.edu → utexas-my.sharepoint.com/personal/bbooth_utexas_edu
                    user_part = email.split("@")[0]
                    domain_part = org.replace(".", "_")
                    return f"https://{org.split('.')[0]}-my.sharepoint.com/personal/{user_part}_{domain_part}/_layouts/15/onedrive.aspx"
                return f"https://{org.split('.')[0]}-my.sharepoint.com/"
        except Exception:
            pass

        # Fallback: generic OneDrive (will redirect to org login if needed)
        return "https://onedrive.live.com/"

    def _upload_to_onedrive(
        self,
        page,
        context,
        local_path: Path,
        remote_name: str,
        target_folder: str,
    ) -> UploadResult:
        """Navigate to OneDrive folder and upload a file."""

        onedrive_url = self._resolve_onedrive_url()
        page.goto(onedrive_url, wait_until="domcontentloaded", timeout=30000)

        # Handle login if needed
        if self._needs_login(page):
            self._do_login(page)

        page.wait_for_timeout(3000)

        # Navigate to target folder (create if needed)
        self._navigate_to_folder(page, target_folder)

        # Check if file already exists (update vs create)
        existing = page.query_selector(
            f"[data-automationid='FieldRenderer-name']:has-text('{remote_name}')"
        )

        if existing:
            # File exists — delete old version first, then upload new
            # (OneDrive web doesn't have a clean "replace" — upload creates duplicates)
            existing.click(button="right")
            page.wait_for_timeout(500)
            delete_btn = page.query_selector(
                "button:has-text('Delete'), [data-automationid='deleteCommand']"
            )
            if delete_btn:
                delete_btn.click()
                # Confirm deletion
                confirm = page.query_selector(
                    "button:has-text('Delete'), .ms-Dialog-action button"
                )
                if confirm:
                    confirm.click()
                page.wait_for_timeout(1000)

        # Upload the file
        # OneDrive web UI: click "Upload" → "Files" → file picker
        upload_btn = page.query_selector(
            "button:has-text('Upload'), "
            "[data-automationid='uploadCommand'], "
            "button[aria-label='Upload']"
        )

        if upload_btn:
            upload_btn.click()
            page.wait_for_timeout(500)

            # Click "Files" option
            files_option = page.query_selector(
                "button:has-text('Files'), "
                "[data-automationid='uploadFilesCommand']"
            )
            if files_option:
                files_option.click()

            # Handle file picker via Playwright's file chooser
            with page.expect_file_chooser() as fc_info:
                # The file chooser should already be triggered
                pass
            file_chooser = fc_info.value
            file_chooser.set_files(str(local_path))

            page.wait_for_timeout(3000)  # Wait for upload

            # Get the URL of the uploaded file
            url = self._get_file_url(page, remote_name)

            return UploadResult(
                success=True,
                url=url,
                storage_id=remote_name,
                metadata={"folder": target_folder, "method": "browser"},
            )

        # Fallback: drag-and-drop upload
        # Some OneDrive views support this natively
        return UploadResult(
            success=False,
            url="",
            error="Upload button not found. OneDrive UI may have changed.",
        )

    def _needs_login(self, page) -> bool:
        url = page.url
        return (
            "login.microsoftonline.com" in url
            or "login.live.com" in url
            or "login.microsoft.com" in url
        )

    def _do_login(self, page) -> None:
        if self.headless:
            raise RuntimeError(
                "Login required but running headless. Run with --headed first."
            )
        print("\n  Microsoft login required.")
        print("  Complete login + MFA in the browser window.\n")
        try:
            page.wait_for_url(
                re.compile(r"(onedrive|sharepoint)\."),
                timeout=300_000,
            )
            print("  ✓ Login successful.\n")
        except Exception:
            raise RuntimeError("Login timed out (5 minute limit).")

    def _navigate_to_folder(self, page, folder_path: str) -> None:
        """Navigate to a folder in OneDrive, creating it if needed."""
        parts = [p for p in folder_path.strip("/").split("/") if p]

        for part in parts:
            folder_link = page.query_selector(
                f"[data-automationid='FieldRenderer-name']:has-text('{part}')"
            )
            if folder_link:
                folder_link.click()
                page.wait_for_timeout(1500)
            else:
                # Create the folder
                new_btn = page.query_selector(
                    "button:has-text('New'), [data-automationid='newCommand']"
                )
                if new_btn:
                    new_btn.click()
                    page.wait_for_timeout(500)
                    folder_option = page.query_selector(
                        "button:has-text('Folder'), [data-automationid='newFolderCommand']"
                    )
                    if folder_option:
                        folder_option.click()
                        page.wait_for_timeout(500)
                        # Type folder name
                        name_input = page.query_selector(
                            "input[type='text'], [data-automationid='TextField']"
                        )
                        if name_input:
                            name_input.fill(part)
                            page.keyboard.press("Enter")
                            page.wait_for_timeout(1500)
                            # Navigate into the new folder
                            new_folder = page.query_selector(
                                f"[data-automationid='FieldRenderer-name']:has-text('{part}')"
                            )
                            if new_folder:
                                new_folder.click()
                                page.wait_for_timeout(1000)

    def _get_file_url(self, page, filename: str) -> str:
        """Try to get the sharing URL for an uploaded file."""
        file_link = page.query_selector(
            f"[data-automationid='FieldRenderer-name']:has-text('{filename}')"
        )
        if file_link:
            # Right-click → "Share" or "Copy link"
            file_link.click(button="right")
            page.wait_for_timeout(500)

            share_btn = page.query_selector(
                "button:has-text('Share'), [data-automationid='shareCommand']"
            )
            if share_btn:
                share_btn.click()
                page.wait_for_timeout(1000)

                copy_link = page.query_selector(
                    "button:has-text('Copy link'), [data-automationid='copyLinkCommand']"
                )
                if copy_link:
                    copy_link.click()
                    page.wait_for_timeout(500)
                    # Close share dialog
                    close = page.query_selector("button[aria-label='Close']")
                    if close:
                        close.click()
                    # The URL is now in clipboard — we can't access it directly
                    # Return the page URL as a fallback
                    return page.url

            # Close context menu
            page.keyboard.press("Escape")

        return page.url

    def clear_session(self) -> None:
        """Clear saved browser session."""
        state_file = self.session_dir / "state.json"
        if state_file.exists():
            state_file.unlink()

    # StorageProvider interface methods

    def list_files(self, folder: str = "") -> list[StorageEntry]:
        return []  # Not implemented for browser provider

    def download(self, remote_path: str, local_path: Path) -> bool:
        return False  # Use OneDrive web UI directly

    def delete(self, remote_path: str) -> bool:
        return False  # Not implemented

    def get_canonical_url(self, storage_id: str) -> str:
        return ""  # URL returned during upload

    def list_artifacts(self, folder: str = "") -> list[dict]:
        return []  # Not implemented for browser provider

    def move(self, source: str, destination: str) -> bool:
        return False  # Not implemented for browser provider


# Register with the publisher factory
try:
    PublisherFactory.register_storage(
        "onedrive-browser",
        OneDriveBrowserStorageProvider,
    )
except Exception:
    pass  # Factory may not be initialized yet
