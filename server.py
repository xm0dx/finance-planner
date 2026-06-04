#!/usr/bin/env python3
"""Tiny persistence backend for the Money Plan page.

Stores the whole app state (the mick_* localStorage keys) as one JSON blob in
/data/state.json on a Docker volume, so it survives reboots and is shared
across every device. No dependencies — Python standard library only.

  GET  /state  -> returns the saved JSON ({} if nothing saved yet)
  PUT  /state  -> overwrites the saved JSON (body must be valid JSON)
  POST /state  -> same as PUT

nginx proxies /api/ here, so the browser calls /api/state same-origin.
"""
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DATA = "/data/state.json"
MAX_BYTES = 5 * 1024 * 1024  # 5 MB cap — plenty for a budget, blocks abuse
LOCK = threading.Lock()


def read_state():
    try:
        with open(DATA, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return b"{}"


def write_state(raw):
    """Atomic write: temp file + fsync + rename, so a crash mid-write can't
    corrupt the saved state."""
    with LOCK:
        tmp = DATA + ".tmp"
        with open(tmp, "wb") as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, DATA)


class Handler(BaseHTTPRequestHandler):
    def _ok_path(self):
        return self.path.split("?")[0].rstrip("/") in ("", "/state")

    def _head(self, code, length=0, ctype="application/json"):
        self.send_response(code)
        if length:
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(length))
        # Same-origin via nginx; CORS kept permissive in case it's hit directly.
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,PUT,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._head(204)

    def do_GET(self):
        if not self._ok_path():
            self._head(404)
            return
        body = read_state()
        self._head(200, len(body))
        self.wfile.write(body)

    def do_PUT(self):
        self._write()

    def do_POST(self):
        self._write()

    def _write(self):
        if not self._ok_path():
            self._head(404)
            return
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_BYTES:
            self._head(413)
            return
        raw = self.rfile.read(n)
        try:
            json.loads(raw)  # reject anything that isn't valid JSON
        except Exception:
            self._head(400)
            return
        write_state(raw)
        self._head(200, 2)
        self.wfile.write(b"ok")

    def log_message(self, *args):
        pass  # quiet — Dozzle/compose logs would otherwise fill with noise


if __name__ == "__main__":
    os.makedirs("/data", exist_ok=True)
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
