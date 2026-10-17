from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_message_request import CreateMessageRequest
from ...models.create_message_response import CreateMessageResponse
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: str,
    task_id: str,
    *,
    body: CreateMessageRequest,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/workspaces/{workspace_id}/tasks/{task_id}/messages".format(
            workspace_id=quote(str(workspace_id), safe=""),
            task_id=quote(str(task_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateMessageResponse | Error | None:
    if response.status_code == 202:
        response_202 = CreateMessageResponse.from_dict(response.json())

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
) -> Response[CreateMessageResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: str,
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateMessageRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[CreateMessageResponse | Error]:
    """Send a message

     Sends a follow-up on a task and returns `202` with the message's id.

    Any member of the workspace can follow up on a task started from the API, CLI, MCP or dashboard.
    Follow up on other tasks, such as Linear or GitHub issues, where they started; here they return `409
    not_an_api_task`. A task that has been idle for a while picks up again when you follow up.

    A message sent while the agent is working doesn't change the current turn. It waits and runs as the
    next turn. A message isn't refused when the workspace is running its limit of tasks: its turn takes
    a place in the queue, and if the queue is full, the refusal appears in the task's conversation
    instead.

    Send an `Idempotency-Key` so a retry is safe: a message retried with the same key is sent once. Keys
    belong to their sender, so two people using the same key send two messages. The key becomes the
    message's `messageId`.

    If Sinatra saves the message but can't hand it to the agent yet, it answers `503 unavailable` with
    the `messageId`. Retry with that `messageId` as the `Idempotency-Key`, so the message is sent once.

    Args:
        workspace_id (str):
        task_id (str):
        idempotency_key (str | Unset):
        body (CreateMessageRequest): A message to send on a task.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateMessageResponse | Error]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        task_id=task_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateMessageRequest,
    idempotency_key: str | Unset = UNSET,
) -> CreateMessageResponse | Error | None:
    """Send a message

     Sends a follow-up on a task and returns `202` with the message's id.

    Any member of the workspace can follow up on a task started from the API, CLI, MCP or dashboard.
    Follow up on other tasks, such as Linear or GitHub issues, where they started; here they return `409
    not_an_api_task`. A task that has been idle for a while picks up again when you follow up.

    A message sent while the agent is working doesn't change the current turn. It waits and runs as the
    next turn. A message isn't refused when the workspace is running its limit of tasks: its turn takes
    a place in the queue, and if the queue is full, the refusal appears in the task's conversation
    instead.

    Send an `Idempotency-Key` so a retry is safe: a message retried with the same key is sent once. Keys
    belong to their sender, so two people using the same key send two messages. The key becomes the
    message's `messageId`.

    If Sinatra saves the message but can't hand it to the agent yet, it answers `503 unavailable` with
    the `messageId`. Retry with that `messageId` as the `Idempotency-Key`, so the message is sent once.

    Args:
        workspace_id (str):
        task_id (str):
        idempotency_key (str | Unset):
        body (CreateMessageRequest): A message to send on a task.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateMessageResponse | Error
    """

    return sync_detailed(
        workspace_id=workspace_id,
        task_id=task_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateMessageRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[CreateMessageResponse | Error]:
    """Send a message

     Sends a follow-up on a task and returns `202` with the message's id.

    Any member of the workspace can follow up on a task started from the API, CLI, MCP or dashboard.
    Follow up on other tasks, such as Linear or GitHub issues, where they started; here they return `409
    not_an_api_task`. A task that has been idle for a while picks up again when you follow up.

    A message sent while the agent is working doesn't change the current turn. It waits and runs as the
    next turn. A message isn't refused when the workspace is running its limit of tasks: its turn takes
    a place in the queue, and if the queue is full, the refusal appears in the task's conversation
    instead.

    Send an `Idempotency-Key` so a retry is safe: a message retried with the same key is sent once. Keys
    belong to their sender, so two people using the same key send two messages. The key becomes the
    message's `messageId`.

    If Sinatra saves the message but can't hand it to the agent yet, it answers `503 unavailable` with
    the `messageId`. Retry with that `messageId` as the `Idempotency-Key`, so the message is sent once.

    Args:
        workspace_id (str):
        task_id (str):
        idempotency_key (str | Unset):
        body (CreateMessageRequest): A message to send on a task.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateMessageResponse | Error]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        task_id=task_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateMessageRequest,
    idempotency_key: str | Unset = UNSET,
) -> CreateMessageResponse | Error | None:
    """Send a message

     Sends a follow-up on a task and returns `202` with the message's id.

    Any member of the workspace can follow up on a task started from the API, CLI, MCP or dashboard.
    Follow up on other tasks, such as Linear or GitHub issues, where they started; here they return `409
    not_an_api_task`. A task that has been idle for a while picks up again when you follow up.

    A message sent while the agent is working doesn't change the current turn. It waits and runs as the
    next turn. A message isn't refused when the workspace is running its limit of tasks: its turn takes
    a place in the queue, and if the queue is full, the refusal appears in the task's conversation
    instead.

    Send an `Idempotency-Key` so a retry is safe: a message retried with the same key is sent once. Keys
    belong to their sender, so two people using the same key send two messages. The key becomes the
    message's `messageId`.

    If Sinatra saves the message but can't hand it to the agent yet, it answers `503 unavailable` with
    the `messageId`. Retry with that `messageId` as the `Idempotency-Key`, so the message is sent once.

    Args:
        workspace_id (str):
        task_id (str):
        idempotency_key (str | Unset):
        body (CreateMessageRequest): A message to send on a task.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateMessageResponse | Error
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            task_id=task_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
