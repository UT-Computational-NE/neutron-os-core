"""HTTP ingestion server for neut sense.

Dead-simple way to get files into the inbox from any device on the LAN.
Uses only stdlib (http.server) — zero external dependencies.

Endpoints:
    POST /upload    Upload a file (auto-routed by extension)
    POST /note      Submit a text note (becomes inbox/raw/note_TIMESTAMP.md)
    GET  /status    Returns inbox counts as JSON
    GET  /          Minimal HTML upload page (drag-and-drop, text note box)

File routing by extension:
    .m4a, .mp3, .wav, .ogg, .webm  →  inbox/raw/voice/
    .vtt, .srt                       →  inbox/raw/teams/
    .md, .txt                        →  inbox/raw/
    everything else                  →  inbox/raw/other/

Usage:
    neut sense serve [--port 8765] [--host 0.0.0.0]
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs

# Resolve inbox path relative to tools/agents/
_AGENTS_DIR = Path(__file__).resolve().parent.parent
INBOX_RAW = _AGENTS_DIR / "inbox" / "raw"

# Extension → subdirectory routing
ROUTE_MAP: dict[str, str] = {
    ".m4a": "voice",
    ".mp3": "voice",
    ".wav": "voice",
    ".ogg": "voice",
    ".webm": "voice",
    ".vtt": "teams",
    ".srt": "teams",
    ".md": "",      # root of inbox/raw
    ".txt": "",
}

UPLOAD_PAGE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>neut sense — inbox</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; color: #222; }
  h1 { font-size: 1.3rem; margin-bottom: 1rem; }
  .drop-zone {
    border: 2px dashed #aaa; border-radius: 8px; padding: 2rem; text-align: center;
    cursor: pointer; margin-bottom: 1.5rem; transition: border-color 0.2s;
  }
  .drop-zone.active { border-color: #0066cc; background: #f0f7ff; }
  .drop-zone input { display: none; }
  textarea { width: 100%; height: 120px; border: 1px solid #ccc; border-radius: 6px; padding: 0.75rem; font-family: inherit; resize: vertical; }
  button { margin-top: 0.5rem; padding: 0.5rem 1.5rem; background: #0066cc; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; }
  button:hover { background: #0052a3; }
  .status { margin-top: 1rem; color: #555; font-size: 0.9rem; }
  .msg { margin-top: 0.75rem; padding: 0.5rem; border-radius: 4px; }
  .msg.ok { background: #e6f4ea; color: #1b7a3d; }
  .msg.err { background: #fce8e6; color: #c5221f; }
  h2 { font-size: 1.1rem; margin-bottom: 0.5rem; }
  section { margin-bottom: 1.5rem; }
</style>
</head>
<body>
<h1>neut sense inbox</h1>

<section>
<h2>Upload file</h2>
<div class="drop-zone" id="dropZone">
  Drop files here or click to browse
  <input type="file" id="fileInput" multiple>
</div>
</section>

<section>
<h2>Quick note</h2>
<textarea id="noteText" placeholder="Type a note..."></textarea>
<br>
<button onclick="submitNote()">Send note</button>
</section>

<div id="feedback"></div>
<div class="status" id="statusLine"></div>

<script>
const dz = document.getElementById('dropZone');
const fi = document.getElementById('fileInput');
const fb = document.getElementById('feedback');

dz.addEventListener('click', () => fi.click());
dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('active'); });
dz.addEventListener('dragleave', () => dz.classList.remove('active'));
dz.addEventListener('drop', e => {
  e.preventDefault(); dz.classList.remove('active');
  uploadFiles(e.dataTransfer.files);
});
fi.addEventListener('change', () => uploadFiles(fi.files));

async function uploadFiles(files) {
  for (const f of files) {
    const form = new FormData();
    form.append('file', f);
    try {
      const r = await fetch('/upload', { method: 'POST', body: form });
      const j = await r.json();
      show(r.ok ? 'ok' : 'err', j.message || j.error);
    } catch(e) { show('err', e.message); }
  }
  refreshStatus();
}

async function submitNote() {
  const text = document.getElementById('noteText').value.trim();
  if (!text) return;
  try {
    const r = await fetch('/note', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: 'text=' + encodeURIComponent(text),
    });
    const j = await r.json();
    show(r.ok ? 'ok' : 'err', j.message || j.error);
    if (r.ok) document.getElementById('noteText').value = '';
  } catch(e) { show('err', e.message); }
  refreshStatus();
}

function show(cls, msg) {
  fb.innerHTML = '<div class="msg ' + cls + '">' + msg + '</div>';
}

async function refreshStatus() {
  try {
    const r = await fetch('/status');
    const j = await r.json();
    const parts = Object.entries(j.counts || {}).map(([k,v]) => k + ': ' + v);
    document.getElementById('statusLine').textContent = 'Inbox: ' + (parts.join(', ') || 'empty');
  } catch(e) {}
}

refreshStatus();
</script>
</body>
</html>
"""


def _parse_multipart(body: bytes, boundary: str) -> tuple[str, bytes]:
    """Parse a multipart/form-data body and extract the first file.

    Returns:
        (filename, file_data) or ("", b"") if no file found.
    """
    boundary_bytes = boundary.encode("utf-8")
    # Parts are separated by --boundary
    parts = body.split(b"--" + boundary_bytes)

    for part in parts:
        if b"Content-Disposition" not in part:
            continue
        # Split headers from body at the double CRLF
        header_end = part.find(b"\r\n\r\n")
        if header_end == -1:
            continue
        headers_section = part[:header_end].decode("utf-8", errors="replace")
        file_body = part[header_end + 4:]  # Skip \r\n\r\n

        # Remove trailing \r\n
        if file_body.endswith(b"\r\n"):
            file_body = file_body[:-2]

        # Extract filename
        match = re.search(r'filename="([^"]+)"', headers_section)
        if match:
            return match.group(1), file_body

    return "", b""


class InboxHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the inbox ingestion server."""

    inbox_root: Path = INBOX_RAW

    def do_GET(self):
        if self.path == "/status":
            self._handle_status()
        elif self.path == "/" or self.path == "":
            self._serve_upload_page()
        else:
            self._respond(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/upload":
            self._handle_upload()
        elif self.path == "/note":
            self._handle_note()
        else:
            self._respond(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def _handle_status(self):
        """Return inbox file counts as JSON."""
        counts: dict[str, int] = {}
        root = self.inbox_root
        if root.exists():
            for child in root.iterdir():
                if child.is_dir():
                    n = sum(1 for f in child.rglob("*") if f.is_file() and f.name != ".gitkeep")
                    if n:
                        counts[child.name] = n
                elif child.is_file() and child.name != ".gitkeep":
                    counts["root"] = counts.get("root", 0) + 1
        self._respond(HTTPStatus.OK, {"counts": counts})

    def _serve_upload_page(self):
        """Serve the minimal HTML upload interface."""
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        page = UPLOAD_PAGE.encode("utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def _handle_upload(self):
        """Handle multipart file upload, route by extension."""
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._respond(HTTPStatus.BAD_REQUEST, {"error": "Expected multipart/form-data"})
            return

        # Extract boundary from Content-Type
        match = re.search(r"boundary=(.+)", content_type)
        if not match:
            self._respond(HTTPStatus.BAD_REQUEST, {"error": "No boundary in Content-Type"})
            return
        boundary = match.group(1).strip()

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        # Parse multipart manually (cgi module removed in Python 3.13)
        filename, file_data = _parse_multipart(body, boundary)

        if not filename:
            self._respond(HTTPStatus.BAD_REQUEST, {"error": "No file provided"})
            return

        filename = Path(filename).name  # Sanitize
        ext = Path(filename).suffix.lower()
        subdir = ROUTE_MAP.get(ext, "other")

        dest_dir = self.inbox_root / subdir if subdir else self.inbox_root
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / filename

        # Avoid overwriting — append timestamp if exists
        if dest.exists():
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            stem = dest.stem
            dest = dest_dir / f"{stem}_{ts}{ext}"

        dest.write_bytes(file_data)

        route_label = subdir if subdir else "root"
        self._respond(HTTPStatus.OK, {
            "message": f"Saved {filename} → inbox/raw/{route_label}/ ({len(file_data)} bytes)",
            "path": str(dest.relative_to(self.inbox_root)),
        })

    def _handle_note(self):
        """Handle text note submission."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self._respond(HTTPStatus.BAD_REQUEST, {"error": "Empty request"})
            return

        body = self.rfile.read(content_length).decode("utf-8")
        params = parse_qs(body)
        text = params.get("text", [""])[0].strip()

        if not text:
            self._respond(HTTPStatus.BAD_REQUEST, {"error": "No text provided"})
            return

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
        self.inbox_root.mkdir(parents=True, exist_ok=True)
        dest = self.inbox_root / f"note_{ts}.md"
        dest.write_text(f"# Note — {ts}\n\n{text}\n", encoding="utf-8")

        self._respond(HTTPStatus.OK, {
            "message": f"Note saved as {dest.name}",
            "path": dest.name,
        })

    def _respond(self, status: HTTPStatus, data: dict):
        """Send a JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        payload = json.dumps(data).encode("utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        """Override to use a cleaner log format."""
        print(f"  [{self.log_date_time_string()}] {format % args}")


def create_server(
    host: str = "0.0.0.0",
    port: int = 8765,
    inbox_root: Optional[Path] = None,
) -> HTTPServer:
    """Create and return a configured HTTP server (not yet started).

    Args:
        host: Bind address (0.0.0.0 for LAN access).
        port: Port number.
        inbox_root: Override inbox path (for testing).
    """
    if inbox_root is not None:
        InboxHandler.inbox_root = inbox_root
    else:
        InboxHandler.inbox_root = INBOX_RAW

    server = HTTPServer((host, port), InboxHandler)
    return server


def run_server(host: str = "0.0.0.0", port: int = 8765):
    """Start the inbox server (blocking)."""
    INBOX_RAW.mkdir(parents=True, exist_ok=True)

    server = create_server(host, port)
    print(f"neut sense serve — inbox ingestion server")
    print(f"  Listening on http://{host}:{port}")
    print(f"  Inbox:      {INBOX_RAW}")
    print(f"  Upload:     POST /upload  (multipart file)")
    print(f"  Note:       POST /note    (text=...)")
    print(f"  Status:     GET  /status")
    print(f"  UI:         GET  /")
    print()
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
