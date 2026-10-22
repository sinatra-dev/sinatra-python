from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_task_request import CreateTaskRequest
from ...models.create_task_response import CreateTaskResponse
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: str,
    *,
    body: CreateTaskRequest,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/workspaces/{workspace_id}/tasks".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateTaskResponse | Error | None:
    if response.status_code == 202:
        response_202 = CreateTaskResponse.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CreateTaskResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateTaskRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[CreateTaskResponse | Error]:
    """Start a task

     Starts a task and returns `202` with the task and the id of your first message. The task runs like
    any other: it gets a sandbox, can open a pull request, and shows up in the dashboard.

    Only `prompt` is required. `title` defaults to the prompt's first line, up to 80 characters. `repo`
    is optional: omit it to let the agent choose a repository.

    Before it makes the task, Sinatra checks that the workspace is connected to GitHub when the start
    names a repository (without GitHub a task that names none can still answer, research or plan), that
    billing allows the task, and that the queue has room. A refusal says which in its `error` code, and
    a retry with the same key of a start that already made its task is never refused.

    Send an `Idempotency-Key` so a retry is safe. A start retried with the same key returns the same
    task and never starts a second one. The same key with a different prompt, or a different repository
    or title if you send them, is `409 idempotency_conflict`. Keys belong to the person who sent them.
    The key becomes the first message's `messageId`.

    If Sinatra saves your request but can't hand it to the agent yet, it answers `503 unavailable` with
    the new `taskId` and `messageId`. Retry with the same key, or send a message on that task, which
    sends your prompt first.

    A task started this way counts against the workspace's plan like any other. A running turn takes one
    of the plan's tasks at a time; past that it's queued. See [How the queue
    works](https://docs.sinatra.dev/docs/managed/billing#how-the-queue-works). It also needs model
    access, like a task delegated from Linear or GitHub. See
    [Models](https://docs.sinatra.dev/docs/configuration/models).

    Args:
        workspace_id (str):
        idempotency_key (str | Unset):
        body (CreateTaskRequest): A task to start.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTaskResponse | Error]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateTaskRequest,
    idempotency_key: str | Unset = UNSET,
) -> CreateTaskResponse | Error | None:
    """Start a task

     Starts a task and returns `202` with the task and the id of your first message. The task runs like
    any other: it gets a sandbox, can open a pull request, and shows up in the dashboard.

    Only `prompt` is required. `title` defaults to the prompt's first line, up to 80 characters. `repo`
    is optional: omit it to let the agent choose a repository.

    Before it makes the task, Sinatra checks that the workspace is connected to GitHub when the start
    names a repository (without GitHub a task that names none can still answer, research or plan), that
    billing allows the task, and that the queue has room. A refusal says which in its `error` code, and
    a retry with the same key of a start that already made its task is never refused.

    Send an `Idempotency-Key` so a retry is safe. A start retried with the same key returns the same
    task and never starts a second one. The same key with a different prompt, or a different repository
    or title if you send them, is `409 idempotency_conflict`. Keys belong to the person who sent them.
    The key becomes the first message's `messageId`.

    If Sinatra saves your request but can't hand it to the agent yet, it answers `503 unavailable` with
    the new `taskId` and `messageId`. Retry with the same key, or send a message on that task, which
    sends your prompt first.

    A task started this way counts against the workspace's plan like any other. A running turn takes one
    of the plan's tasks at a time; past that it's queued. See [How the queue
    works](https://docs.sinatra.dev/docs/managed/billing#how-the-queue-works). It also needs model
    access, like a task delegated from Linear or GitHub. See
    [Models](https://docs.sinatra.dev/docs/configuration/models).

    Args:
        workspace_id (str):
        idempotency_key (str | Unset):
        body (CreateTaskRequest): A task to start.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTaskResponse | Error
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateTaskRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[CreateTaskResponse | Error]:
    """Start a task

     Starts a task and returns `202` with the task and the id of your first message. The task runs like
    any other: it gets a sandbox, can open a pull request, and shows up in the dashboard.

    Only `prompt` is required. `title` defaults to the prompt's first line, up to 80 characters. `repo`
    is optional: omit it to let the agent choose a repository.

    Before it makes the task, Sinatra checks that the workspace is connected to GitHub when the start
    names a repository (without GitHub a task that names none can still answer, research or plan), that
    billing allows the task, and that the queue has room. A refusal says which in its `error` code, and
    a retry with the same key of a start that already made its task is never refused.

    Send an `Idempotency-Key` so a retry is safe. A start retried with the same key returns the same
    task and never starts a second one. The same key with a different prompt, or a different repository
    or title if you send them, is `409 idempotency_conflict`. Keys belong to the person who sent them.
    The key becomes the first message's `messageId`.

    If Sinatra saves your request but can't hand it to the agent yet, it answers `503 unavailable` with
    the new `taskId` and `messageId`. Retry with the same key, or send a message on that task, which
    sends your prompt first.

    A task started this way counts against the workspace's plan like any other. A running turn takes one
    of the plan's tasks at a time; past that it's queued. See [How the queue
    works](https://docs.sinatra.dev/docs/managed/billing#how-the-queue-works). It also needs model
    access, like a task delegated from Linear or GitHub. See
    [Models](https://docs.sinatra.dev/docs/configuration/models).

    Args:
        workspace_id (str):
        idempotency_key (str | Unset):
        body (CreateTaskRequest): A task to start.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateTaskResponse | Error]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateTaskRequest,
    idempotency_key: str | Unset = UNSET,
) -> CreateTaskResponse | Error | None:
    """Start a task

     Starts a task and returns `202` with the task and the id of your first message. The task runs like
    any other: it gets a sandbox, can open a pull request, and shows up in the dashboard.

    Only `prompt` is required. `title` defaults to the prompt's first line, up to 80 characters. `repo`
    is optional: omit it to let the agent choose a repository.

    Before it makes the task, Sinatra checks that the workspace is connected to GitHub when the start
    names a repository (without GitHub a task that names none can still answer, research or plan), that
    billing allows the task, and that the queue has room. A refusal says which in its `error` code, and
    a retry with the same key of a start that already made its task is never refused.

    Send an `Idempotency-Key` so a retry is safe. A start retried with the same key returns the same
    task and never starts a second one. The same key with a different prompt, or a different repository
    or title if you send them, is `409 idempotency_conflict`. Keys belong to the person who sent them.
    The key becomes the first message's `messageId`.

    If Sinatra saves your request but can't hand it to the agent yet, it answers `503 unavailable` with
    the new `taskId` and `messageId`. Retry with the same key, or send a message on that task, which
    sends your prompt first.

    A task started this way counts against the workspace's plan like any other. A running turn takes one
    of the plan's tasks at a time; past that it's queued. See [How the queue
    works](https://docs.sinatra.dev/docs/managed/billing#how-the-queue-works). It also needs model
    access, like a task delegated from Linear or GitHub. See
    [Models](https://docs.sinatra.dev/docs/configuration/models).

    Args:
        workspace_id (str):
        idempotency_key (str | Unset):
        body (CreateTaskRequest): A task to start.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateTaskResponse | Error
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
