"""Wrapper tests, against the local stub server (stub_server.py), never Prism or the live API."""

from __future__ import annotations

import re
import time
from collections.abc import Iterator
from typing import Any

import httpx
import pytest
from stub_server import FakeClock, Reply, Stub

from sinatra_dev import Sinatra, SinatraError
from sinatra_dev._generated.api.tasks import tasks_get

WS = "ws_1"
UUID_V4 = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
ME = {"user": {"id": "user_1", "githubLogin": "octo", "name": "Octo"}, "workspaces": []}


def task(**overrides: Any) -> dict[str, Any]:
    return {
        "id": "task_1",
        "status": "implementing",
        "source": "api",
        "title": "Fix the flaky test",
        "repo": "acme/web",
        "pullRequest": None,
        "queued": False,
        "createdAt": "2026-10-16T12:00:00.000Z",
        "lastActivityAt": None,
        "url": "https://app.sinatra.dev/tasks/task_1",
        **overrides,
    }


def message(id: str) -> dict[str, Any]:
    return {
        "id": id,
        "messageId": None,
        "role": "agent",
        "kind": "response",
        "body": f"entry {id}",
        "createdAt": "2026-10-16T12:00:00.000Z",
    }


@pytest.fixture
def sinatra(stub: Stub) -> Iterator[Sinatra]:
    with Sinatra(token="sntr_test", base_url=stub.url) as client:
        yield client


class TestRetries:
    def test_retries_reuse_the_idempotency_key(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(
            Reply(503, {"error": "unavailable", "taskId": "task_1", "messageId": "m"}),
            Reply(202, {"task": task(), "messageId": "m"}),
        )

        created = sinatra.tasks.create(WS, "Fix the flaky test")

        assert created.task.id == "task_1"
        keys = [r.headers.get("idempotency-key") for r in stub.requests]
        assert len(keys) == 2
        assert keys[0] is not None and UUID_V4.match(keys[0])
        assert keys[1] == keys[0]

    def test_a_key_you_pass_is_sent_on_every_attempt(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(503, {"error": "unavailable"}), Reply(202, {"messageId": "mine-1"}))

        sinatra.messages.create(WS, "task_1", "and the docs", idempotency_key="mine-1")

        assert [r.headers.get("idempotency-key") for r in stub.requests] == ["mine-1", "mine-1"]

    def test_each_call_gets_its_own_key(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(202, {"messageId": "a"}), Reply(202, {"messageId": "b"}))

        sinatra.messages.create(WS, "task_1", "one")
        sinatra.messages.create(WS, "task_1", "two")

        first, second = (r.headers.get("idempotency-key") for r in stub.requests)
        assert first is not None and UUID_V4.match(first)
        assert second is not None and UUID_V4.match(second)
        assert second != first

    def test_429_honours_retry_after(self, stub: Stub, clock: FakeClock, sinatra: Sinatra) -> None:
        stub.reply(Reply(429, {"error": "rate_limited"}, {"Retry-After": "1"}), Reply(200, ME))

        me = sinatra.me.get()

        assert me.user.id == "user_1"
        assert len(stub.requests) == 2
        waited = stub.requests[1].at - stub.requests[0].at
        assert 1.0 <= waited < 1.5

    def test_retry_after_is_capped_at_60_seconds(self, stub: Stub, clock: FakeClock, sinatra: Sinatra) -> None:
        stub.reply(Reply(429, {"error": "rate_limited"}, {"Retry-After": "3600"}), Reply(200, ME))

        sinatra.me.get()

        assert clock.sleeps == [60.0]

    def test_503_backs_off_and_gives_up_after_3_retries(self, stub: Stub, clock: FakeClock, sinatra: Sinatra) -> None:
        stub.reply(*(Reply(503, {"error": "unavailable"}) for _ in range(4)))

        with pytest.raises(SinatraError) as raised:
            sinatra.tasks.get(WS, "task_1")

        assert raised.value.status == 503
        assert len(stub.requests) == 4
        assert clock.sleeps == [0.5, 1.0, 2.0]

    def test_500_is_not_retried(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(500, {"error": "internal_error", "reason": "boom"}))

        with pytest.raises(SinatraError) as raised:
            sinatra.tasks.stop(WS, "task_1")

        assert len(stub.requests) == 1
        assert raised.value.status == 500

    def test_tasks_stop_retries_503_but_not_429(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(503, {"error": "unavailable"}), Reply(202, {"accepted": True}))

        stopped = sinatra.tasks.stop(WS, "task_1")

        assert stopped.accepted is True
        assert len(stub.requests) == 2

        stub.reply(Reply(429, {"error": "rate_limited"}, {"Retry-After": "0"}))
        with pytest.raises(SinatraError) as raised:
            sinatra.tasks.stop(WS, "task_1")
        assert raised.value.status == 429
        assert len(stub.requests) == 3

    def test_a_post_without_an_idempotency_key_is_not_retried(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(503, {"error": "unavailable"}))

        with pytest.raises(SinatraError) as raised:
            sinatra.tickets.delegate(WS, source="linear", id="ENG-1")

        assert raised.value.status == 503
        assert len(stub.requests) == 1


class TestDecoding:
    def test_unknown_status_decodes(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(200, task(status="teleporting", source="carrier_pigeon", brandNewField=1)))

        got = sinatra.tasks.get(WS, "task_1")

        assert got.status == "teleporting"
        assert got.source == "carrier_pigeon"
        assert got.additional_properties == {"brandNewField": 1}

    def test_unknown_error_code_surfaces(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(409, {"error": "brand_new", "reason": "x"}, {"x-request-id": "req_9"}))

        with pytest.raises(SinatraError) as raised:
            sinatra.messages.create(WS, "task_1", "hi")

        err = raised.value
        assert err.status == 409
        assert err.code == "brand_new"
        assert err.reason == "x"
        assert err.request_id == "req_9"
        assert err.body == {"error": "brand_new", "reason": "x"}
        assert len(stub.requests) == 1

    def test_an_error_without_a_json_body_still_surfaces_its_status(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(502, "<html>bad gateway</html>", {"content-type": "text/html"}))

        with pytest.raises(SinatraError) as raised:
            sinatra.tasks.get(WS, "task_1")

        assert raised.value.status == 502
        assert raised.value.code == "http_error"
        assert raised.value.body == "<html>bad gateway</html>"


class TestRequests:
    def test_bodyless_requests_send_no_content_type(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(202, {"accepted": True}), Reply(204), Reply(200, task()))

        sinatra.tasks.stop(WS, "task_1")
        sinatra.me.revoke_token()
        sinatra.tasks.get(WS, "task_1")

        assert [f"{r.method} {r.path}" for r in stub.requests] == [
            "POST /v1/workspaces/ws_1/tasks/task_1/stop",
            "DELETE /v1/me/token",
            "GET /v1/workspaces/ws_1/tasks/task_1",
        ]
        for r in stub.requests:
            assert "content-type" not in r.headers
            assert r.body == b""

    def test_requests_with_a_body_send_json(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(202, {"task": task(), "messageId": "m"}))

        sinatra.tasks.create(WS, "Fix it", repo="acme/web")

        assert stub.requests[0].headers["content-type"] == "application/json"
        assert stub.requests[0].json() == {"prompt": "Fix it", "repo": "acme/web"}

    def test_path_segments_are_encoded(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(Reply(200, task()))

        sinatra.tasks.get("ws/1", "../me")

        assert stub.requests[0].path == "/v1/workspaces/ws%2F1/tasks/..%2Fme"

    def test_a_generated_request_with_parts_the_client_doesnt_send_is_refused(
        self, stub: Stub, sinatra: Sinatra, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # A generator bump that starts building requests with, say, `files` or
        # `content` must not have those silently dropped.
        real = tasks_get._get_kwargs

        def with_files(workspace_id: str, task_id: str) -> dict[str, Any]:
            return {**real(workspace_id, task_id), "files": {"upload": b"x"}}

        monkeypatch.setattr(tasks_get, "_get_kwargs", with_files)

        with pytest.raises(RuntimeError, match="files"):
            sinatra.tasks.get(WS, "task_1")
        assert stub.requests == []

    def test_the_token_defaults_to_sinatra_token(self, stub: Stub, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("SINATRA_TOKEN", "sntr_from_env")
        stub.reply(Reply(200, ME))

        with Sinatra(base_url=stub.url) as client:
            client.me.get()

        assert stub.requests[0].headers["authorization"] == "Bearer sntr_from_env"

    def test_no_token_is_an_error_before_any_request(self, stub: Stub, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("SINATRA_TOKEN", "")

        with pytest.raises(ValueError, match="SINATRA_TOKEN"):
            Sinatra(base_url=stub.url)
        assert stub.requests == []


class TestTimeouts:
    def test_a_hung_request_times_out(self, stub: Stub) -> None:
        stub.reply(Reply(hang=True), Reply(hang=True))

        with Sinatra(token="sntr_test", base_url=stub.url, timeout=0.2) as client:
            started = time.monotonic()
            with pytest.raises(httpx.TimeoutException):
                client.tasks.get(WS, "task_1")
            assert time.monotonic() - started < 5

            # A per-call timeout overrides the client's.
            started = time.monotonic()
            with pytest.raises(httpx.TimeoutException):
                client.tasks.get(WS, "task_1", timeout=0.05)
            assert time.monotonic() - started < 5

        # Timeouts are never retried.
        assert len(stub.requests) == 2


class TestPagination:
    def test_list_iterator_follows_next_cursor(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(
            Reply(200, {"tasks": [task(id="t1"), task(id="t2")], "nextCursor": "c2"}),
            Reply(200, {"tasks": [task(id="t3")], "nextCursor": None}),
        )

        ids = [t.id for t in sinatra.tasks.list_all(WS, status="pr_open", limit=2)]

        assert ids == ["t1", "t2", "t3"]
        assert len(stub.requests) == 2
        assert "cursor" not in stub.requests[0].query
        assert stub.requests[1].query["cursor"] == ["c2"]
        for r in stub.requests:
            assert r.query["status"] == ["pr_open"]
            assert r.query["limit"] == ["2"]

    def test_message_iterator_follows_next_as_after(self, stub: Stub, sinatra: Sinatra) -> None:
        stub.reply(
            Reply(200, {"messages": [message("e1")], "next": "e1"}),
            Reply(200, {"messages": [message("e2")], "next": None}),
        )

        ids = [m.id for m in sinatra.messages.list_all(WS, "task_1")]

        assert ids == ["e1", "e2"]
        assert "after" not in stub.requests[0].query
        assert stub.requests[1].query["after"] == ["e1"]
