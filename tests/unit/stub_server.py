"""A scripted local HTTP server that records every request, and a fake clock.

The wrapper tests run against this stub, never the live API and never Prism:
they need to script exact status codes and headers and to see the bytes the
client really sent (headers included).
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlsplit


@dataclass
class Reply:
    status: int = 200
    body: Any = None
    headers: dict[str, str] = field(default_factory=dict)
    # Never answer: the client has to give up on its own.
    hang: bool = False


@dataclass
class Recorded:
    method: str
    path: str
    query: dict[str, list[str]]
    headers: dict[str, str]
    body: bytes
    # The fake clock's time when the request arrived.
    at: float

    def json(self) -> Any:
        return json.loads(self.body)


class FakeClock:
    """Stands in for time.sleep in the retry loop: sleeping only moves the clock."""

    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


class Stub:
    def __init__(self, clock: FakeClock) -> None:
        self.clock = clock
        self.requests: list[Recorded] = []
        self._replies: list[Reply] = []
        self._lock = threading.Lock()
        self._release = threading.Event()
        stub = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, format: str, *args: Any) -> None:
                pass

            def _handle(self) -> None:
                length = int(self.headers.get("content-length") or 0)
                body = self.rfile.read(length) if length else b""
                url = urlsplit(self.path)
                with stub._lock:
                    stub.requests.append(
                        Recorded(
                            method=self.command,
                            path=url.path,
                            query=parse_qs(url.query),
                            headers={k.lower(): v for k, v in self.headers.items()},
                            body=body,
                            at=stub.clock.now,
                        )
                    )
                    reply = stub._replies.pop(0) if stub._replies else Reply(500, {"error": "no_reply_scripted"})
                if reply.hang:
                    stub._release.wait(10)
                    self.close_connection = True
                    return
                if reply.body is None:
                    payload = b""
                    content_type = None
                elif isinstance(reply.body, str):
                    payload = reply.body.encode()
                    content_type = "text/plain"
                else:
                    payload = json.dumps(reply.body).encode()
                    content_type = "application/json; charset=utf-8"
                self.send_response(reply.status)
                headers = {k.lower(): v for k, v in reply.headers.items()}
                if content_type and "content-type" not in headers:
                    headers["content-type"] = content_type
                for name, value in headers.items():
                    self.send_header(name, value)
                self.send_header("content-length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            do_GET = do_POST = do_DELETE = _handle

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._server.daemon_threads = True
        self._thread = threading.Thread(target=self._server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        self._thread.start()
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}"

    def reply(self, *replies: Reply) -> None:
        with self._lock:
            self._replies.extend(replies)

    def close(self) -> None:
        self._release.set()
        self._server.shutdown()
        self._server.server_close()
