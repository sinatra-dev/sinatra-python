"""Smoke test for an installed sinatra-dev (run by scripts/smoke.sh in a
clean venv with only the built wheel): imports the package from site-packages
and makes real requests to a local server."""

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import sinatra_dev
from sinatra_dev import Sinatra, SinatraError

# A minimal valid Task from openapi.json, so a field the API newly requires
# can't break the smoke test (tests/unit/spec_objects.py: standard library only).
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests" / "unit"))
from spec_objects import spec_object

TASK = spec_object("Task", id="task_1", status="teleporting")


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args: object) -> None:
        pass

    def do_GET(self) -> None:
        ok = self.path == "/v1/workspaces/ws_1/tasks/task_1"
        body = json.dumps(TASK if ok else {"error": "not_found", "reason": "No such task."}).encode()
        self.send_response(200 if ok else 404)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{server.server_address[1]}"

package = Path(sinatra_dev.__file__).parent
assert "site-packages" in package.parts, f"imported from {package}, not an installed wheel"
assert (package / "py.typed").is_file(), "py.typed is missing"

with Sinatra(token="sntr_smoke", base_url=url) as sinatra:
    task = sinatra.tasks.get("ws_1", "task_1")
    assert task.status == "teleporting", task
    try:
        sinatra.tasks.get("ws_1", "nope")
    except SinatraError as err:
        assert (err.status, err.code) == (404, "not_found"), err
    else:
        raise AssertionError("expected a SinatraError")
server.shutdown()
print(f"smoke ok: sinatra-dev from {package}")
