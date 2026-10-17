"""Contract tests: every operation, sent through the wrapper, against a Prism
mock of the committed openapi.json.

Prism runs with --errors, so a request that doesn't match the spec (path,
query, headers, body, auth) is refused and the call raises. Started by
scripts/contract.sh.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import httpx
import pytest

from sinatra_dev import Sinatra, SinatraError

BASE_URL = os.environ.get("SINATRA_CONTRACT_URL", "")
if not BASE_URL:
    raise RuntimeError("SINATRA_CONTRACT_URL is not set: run `bash scripts/contract.sh`")

WS = "ws_contract"
TASK = "task_contract"


@pytest.fixture(scope="module")
def sinatra() -> Iterator[Sinatra]:
    with Sinatra(token="sntr_contract", base_url=BASE_URL) as client:
        yield client


class TestEveryOperationMatchesTheSpec:
    def test_me_get(self, sinatra: Sinatra) -> None:
        me = sinatra.me.get()
        assert isinstance(me.user.id, str)
        assert isinstance(me.workspaces, list)

    def test_me_revoke_token(self, sinatra: Sinatra) -> None:
        sinatra.me.revoke_token()

    def test_tasks_list(self, sinatra: Sinatra) -> None:
        page = sinatra.tasks.list(WS, status="pr_open", limit=100, cursor="opaque")
        assert isinstance(page.tasks, list)

    def test_tasks_create(self, sinatra: Sinatra) -> None:
        created = sinatra.tasks.create(WS, "Fix the flaky test", title="Flaky", repo="acme/web")
        assert isinstance(created.task.id, str)
        assert isinstance(created.message_id, str)

    def test_tasks_create_with_your_own_key(self, sinatra: Sinatra) -> None:
        sinatra.tasks.create(WS, "Fix it", idempotency_key="ci-run-42:fix-it")

    def test_tasks_get(self, sinatra: Sinatra) -> None:
        task = sinatra.tasks.get(WS, TASK)
        assert isinstance(task.status, str)

    def test_tasks_stop(self, sinatra: Sinatra) -> None:
        assert sinatra.tasks.stop(WS, TASK).accepted is True

    def test_messages_create(self, sinatra: Sinatra) -> None:
        sent = sinatra.messages.create(WS, TASK, "Also update the docs")
        assert isinstance(sent.message_id, str)

    def test_messages_list(self, sinatra: Sinatra) -> None:
        page = sinatra.messages.list(WS, TASK, after="entry_1", limit=200)
        assert isinstance(page.messages, list)

    def test_tickets_search(self, sinatra: Sinatra) -> None:
        found = sinatra.tickets.search(WS, q="flaky", repo="acme/web")
        assert isinstance(found.tickets, list)

    def test_tickets_delegate_linear(self, sinatra: Sinatra) -> None:
        assert sinatra.tickets.delegate(WS, source="linear", id="ENG-123").ok is True

    def test_tickets_delegate_github(self, sinatra: Sinatra) -> None:
        assert sinatra.tickets.delegate(WS, source="github", repo="acme/web", number=7).ok is True


class TestTheMockRefusesWhatTheSpecForbids:
    """Guards the suite itself: if Prism stopped validating requests, every
    test above would pass vacuously."""

    def test_a_prompt_that_breaks_the_schema_is_refused(self, sinatra: Sinatra) -> None:
        with pytest.raises(SinatraError) as raised:
            sinatra.tasks.create(WS, "")
        assert raised.value.status >= 400

    def test_a_request_without_a_token_is_refused(self) -> None:
        def drop_auth(request: httpx.Request) -> None:
            del request.headers["authorization"]

        with (
            httpx.Client(event_hooks={"request": [drop_auth]}) as http,
            Sinatra(token="unused", base_url=BASE_URL, http_client=http) as anonymous,
            pytest.raises(SinatraError) as raised,
        ):
            anonymous.me.get()
        assert raised.value.status == 401
