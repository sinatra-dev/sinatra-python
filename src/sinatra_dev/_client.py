"""The Sinatra client: transport, retries and timeouts around the generated code.

The generated package (``_generated``) builds each request (method, encoded
path, query, headers, JSON body) and decodes each response into its attrs
models. This module owns the ``httpx.Client`` and sends every request itself,
so it can retry with the same request and apply a timeout per call, which the
generated ``sync_detailed`` functions can't.
"""

from __future__ import annotations

import os
import uuid
from collections.abc import Callable, Iterator
from importlib.metadata import PackageNotFoundError, version
from types import TracebackType
from typing import Any, Final, Literal, TypeVar

import httpx

from . import _retry
from ._errors import SinatraError
from ._generated.api.me import me_get, me_revoke_token
from ._generated.api.messages import messages_create, messages_list
from ._generated.api.tasks import tasks_create, tasks_get, tasks_list, tasks_stop
from ._generated.api.tickets import tickets_delegate, tickets_search
from ._generated.models import (
    CreateMessageRequest,
    CreateMessageResponse,
    CreateTaskRequest,
    CreateTaskResponse,
    DelegateGithubTicket,
    DelegateLinearTicket,
    DelegateTicketResponse,
    Me,
    Message,
    MessageList,
    StopTaskResponse,
    Task,
    TaskList,
    TicketSearchResult,
)
from ._generated.types import UNSET, Unset

DEFAULT_BASE_URL: Final = "https://api.sinatra.dev"
DEFAULT_TIMEOUT: Final = 60.0
"""Seconds, as an httpx timeout: for connecting, and for each wait for data."""

Timeout = float | httpx.Timeout | None
"""Seconds (or an ``httpx.Timeout``); ``None`` for no timeout."""

T = TypeVar("T")


class _Default:
    """The type of :data:`DEFAULT`: "use the client's timeout"."""

    def __repr__(self) -> str:
        return "DEFAULT"


DEFAULT: Final = _Default()


def _user_agent() -> str:
    try:
        return f"sinatra-dev-python/{version('sinatra-dev')}"
    except PackageNotFoundError:  # pragma: no cover - running from a source tree
        return "sinatra-dev-python"


def _unset(value: T | None) -> T | Unset:
    return UNSET if value is None else value


class Sinatra:
    """A client for the Sinatra API.

    Its namespaces mirror the API's operations: ``me.get`` is ``GET /v1/me``,
    ``tasks.create`` is ``POST /v1/workspaces/{workspaceId}/tasks``.

    Requests that are safe to repeat (GETs, the token DELETE, and starts and
    messages, which always carry an ``Idempotency-Key``) are retried up to 3
    times on ``429`` and ``503``. ``tasks.stop`` is retried on ``503`` only.
    Error responses raise :class:`SinatraError`.

    Use it as a context manager, or call :meth:`close`, to release its
    connections.

    Reference: https://docs.sinatra.dev/docs/api-reference
    """

    def __init__(
        self,
        *,
        token: str | None = None,
        base_url: str | None = None,
        timeout: Timeout = DEFAULT_TIMEOUT,
        http_client: httpx.Client | None = None,
    ) -> None:
        """
        Args:
            token: An API token (``sntr_...``). Defaults to the
                ``SINATRA_TOKEN`` environment variable.
            base_url: Defaults to ``https://api.sinatra.dev``.
            timeout: Seconds each attempt may wait to connect, and for each
                chunk of the response, before httpx raises
                ``httpx.TimeoutException``. Defaults to 60; ``None`` for no
                timeout. A call can override it with its ``timeout`` argument.
            http_client: An ``httpx.Client`` to send requests with, for
                example one with a proxy. The client doesn't close it.
        """
        token = token or os.environ.get("SINATRA_TOKEN") or None
        if not token:
            raise ValueError("No Sinatra API token: pass token=... or set SINATRA_TOKEN.")
        self._transport = _Transport(
            http=http_client or httpx.Client(),
            owns_http=http_client is None,
            base_url=(base_url or DEFAULT_BASE_URL).rstrip("/"),
            headers={"authorization": f"Bearer {token}", "user-agent": _user_agent()},
            timeout=timeout,
        )
        self.me: Final = MeApi(self._transport)
        self.tasks: Final = TasksApi(self._transport)
        self.messages: Final = MessagesApi(self._transport)
        self.tickets: Final = TicketsApi(self._transport)

    def close(self) -> None:
        """Closes the connections, unless the ``httpx.Client`` was yours."""
        self._transport.close()

    def __enter__(self) -> Sinatra:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


class _Transport:
    """Sends a generated request with the client's auth, retries and timeout."""

    def __init__(
        self, *, http: httpx.Client, owns_http: bool, base_url: str, headers: dict[str, str], timeout: Timeout
    ) -> None:
        self.http = http
        self.owns_http = owns_http
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def close(self) -> None:
        if self.owns_http:
            self.http.close()

    def send(self, request: dict[str, Any], retry_on: frozenset[int], timeout: Timeout | _Default) -> httpx.Response:
        """Sends ``request`` (a generated ``_get_kwargs()``) and returns the 2xx
        response. Raises :class:`SinatraError` for any other status."""
        method: str = request["method"]
        url = self.base_url + request["url"]
        headers = {**request.get("headers", {}), **self.headers}
        per_call = self.timeout if isinstance(timeout, _Default) else timeout

        def attempt() -> httpx.Response:
            return self.http.request(
                method.upper(),
                url,
                params=request.get("params"),
                json=request.get("json"),
                headers=headers,
                timeout=per_call,
            )

        response = _retry.with_retries(retry_on, attempt)
        if not response.is_success:
            raise SinatraError.from_response(response)
        return response

    def decode(
        self,
        request: dict[str, Any],
        retry_on: frozenset[int],
        timeout: Timeout | _Default,
        model: Callable[[dict[str, Any]], T],
    ) -> T:
        return model(self.send(request, retry_on, timeout).json())


class MeApi:
    """``me.*``: the token's user."""

    def __init__(self, transport: _Transport) -> None:
        self._t = transport

    def get(self, *, timeout: Timeout | _Default = DEFAULT) -> Me:
        """``me.get``: the user the token acts as, and their workspaces."""
        return self._t.decode(me_get._get_kwargs(), _retry.RETRY_IDEMPOTENT, timeout, Me.from_dict)

    def revoke_token(self, *, timeout: Timeout | _Default = DEFAULT) -> None:
        """``me.revokeToken``: revokes the token this client sends. Later requests get ``401``."""
        self._t.send(me_revoke_token._get_kwargs(), _retry.RETRY_IDEMPOTENT, timeout)


class TasksApi:
    """``tasks.*``: start, follow and stop tasks."""

    def __init__(self, transport: _Transport) -> None:
        self._t = transport

    def list(
        self,
        workspace_id: str,
        *,
        status: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout | _Default = DEFAULT,
    ) -> TaskList:
        """``tasks.list``: one page of the workspace's tasks, most recently active first."""
        request = tasks_list._get_kwargs(
            workspace_id, status=_unset(status), limit=_unset(limit), cursor=_unset(cursor)
        )
        return self._t.decode(request, _retry.RETRY_IDEMPOTENT, timeout, TaskList.from_dict)

    def list_all(
        self,
        workspace_id: str,
        *,
        status: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: Timeout | _Default = DEFAULT,
    ) -> Iterator[Task]:
        """Every task from ``cursor`` on (or from the start), following ``next_cursor``
        page by page. ``limit`` is the page size."""
        while True:
            page = self.list(workspace_id, status=status, limit=limit, cursor=cursor, timeout=timeout)
            yield from page.tasks
            cursor = page.next_cursor
            if not cursor:
                return

    def get(self, workspace_id: str, task_id: str, *, timeout: Timeout | _Default = DEFAULT) -> Task:
        """``tasks.get``: one task, wherever it started."""
        request = tasks_get._get_kwargs(workspace_id, task_id)
        return self._t.decode(request, _retry.RETRY_IDEMPOTENT, timeout, Task.from_dict)

    def create(
        self,
        workspace_id: str,
        prompt: str,
        *,
        title: str | None = None,
        repo: str | None = None,
        idempotency_key: str | None = None,
        timeout: Timeout | _Default = DEFAULT,
    ) -> CreateTaskResponse:
        """``tasks.create``: starts a task. Returns once the task is made, not when
        it's done: poll ``tasks.get`` and ``messages.list`` to follow it.

        ``idempotency_key`` is 1 to 128 printable ASCII characters, with no
        spaces. When you leave it out, the client makes a random UUID. Either
        way, every retry of the call sends the same key, so a retried start
        never starts a second task.
        """
        body = CreateTaskRequest(prompt=prompt, title=_unset(title), repo=_unset(repo))
        key = idempotency_key if idempotency_key is not None else str(uuid.uuid4())
        request = tasks_create._get_kwargs(workspace_id, body=body, idempotency_key=key)
        return self._t.decode(request, _retry.RETRY_IDEMPOTENT, timeout, CreateTaskResponse.from_dict)

    def stop(self, workspace_id: str, task_id: str, *, timeout: Timeout | _Default = DEFAULT) -> StopTaskResponse:
        """``tasks.stop``: stops the task's running turn. A task that isn't running is ``409 not_running``."""
        request = tasks_stop._get_kwargs(workspace_id, task_id)
        return self._t.decode(request, _retry.RETRY_UNAVAILABLE, timeout, StopTaskResponse.from_dict)


class MessagesApi:
    """``messages.*``: a task's conversation."""

    def __init__(self, transport: _Transport) -> None:
        self._t = transport

    def create(
        self,
        workspace_id: str,
        task_id: str,
        text: str,
        *,
        idempotency_key: str | None = None,
        timeout: Timeout | _Default = DEFAULT,
    ) -> CreateMessageResponse:
        """``messages.create``: sends a follow-up on a task started from the API, CLI,
        MCP or dashboard. The idempotency key works as in ``tasks.create``."""
        key = idempotency_key if idempotency_key is not None else str(uuid.uuid4())
        request = messages_create._get_kwargs(
            workspace_id, task_id, body=CreateMessageRequest(text=text), idempotency_key=key
        )
        return self._t.decode(request, _retry.RETRY_IDEMPOTENT, timeout, CreateMessageResponse.from_dict)

    def list(
        self,
        workspace_id: str,
        task_id: str,
        *,
        after: str | None = None,
        limit: int | None = None,
        timeout: Timeout | _Default = DEFAULT,
    ) -> MessageList:
        """``messages.list``: one page of the task's conversation, oldest first. To wait
        for a reply, poll with ``after`` set to the ``id`` of the last entry you read."""
        request = messages_list._get_kwargs(workspace_id, task_id, after=_unset(after), limit=_unset(limit))
        return self._t.decode(request, _retry.RETRY_IDEMPOTENT, timeout, MessageList.from_dict)

    def list_all(
        self,
        workspace_id: str,
        task_id: str,
        *,
        after: str | None = None,
        limit: int | None = None,
        timeout: Timeout | _Default = DEFAULT,
    ) -> Iterator[Message]:
        """Every entry after ``after`` (or from the start), following ``next`` page by page."""
        while True:
            page = self.list(workspace_id, task_id, after=after, limit=limit, timeout=timeout)
            yield from page.messages
            after = page.next_
            if not after:
                return


class TicketsApi:
    """``tickets.*``: Linear and GitHub issues you can delegate."""

    def __init__(self, transport: _Transport) -> None:
        self._t = transport

    def search(
        self,
        workspace_id: str,
        *,
        q: str | None = None,
        repo: str | None = None,
        timeout: Timeout | _Default = DEFAULT,
    ) -> TicketSearchResult:
        """``tickets.search``: open Linear and GitHub issues you could delegate."""
        request = tickets_search._get_kwargs(workspace_id, q=_unset(q), repo=_unset(repo))
        return self._t.decode(request, _retry.RETRY_IDEMPOTENT, timeout, TicketSearchResult.from_dict)

    def delegate(
        self,
        workspace_id: str,
        *,
        source: Literal["linear", "github"],
        id: str | None = None,
        repo: str | None = None,
        number: int | None = None,
        timeout: Timeout | _Default = DEFAULT,
    ) -> DelegateTicketResponse:
        """``tickets.delegate``: hands Sinatra an existing issue as you: a Linear issue
        by ``id`` (``source="linear"``), or a GitHub issue by ``repo`` and
        ``number`` (``source="github"``). Never retried: the operation takes no
        ``Idempotency-Key``."""
        body: DelegateLinearTicket | DelegateGithubTicket
        if source == "linear" and id is not None and repo is None and number is None:
            body = DelegateLinearTicket(source="linear", id=id)
        elif source == "github" and repo is not None and number is not None and id is None:
            body = DelegateGithubTicket(source="github", repo=repo, number=number)
        else:
            raise ValueError(
                'Delegate a Linear issue with source="linear", id=..., or a GitHub issue with '
                'source="github", repo=..., number=...'
            )
        request = tickets_delegate._get_kwargs(workspace_id, body=body)
        return self._t.decode(request, _retry.RETRY_NEVER, timeout, DelegateTicketResponse.from_dict)
