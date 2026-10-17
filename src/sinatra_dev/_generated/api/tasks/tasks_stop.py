from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.stop_task_response import StopTaskResponse
from ...types import Response


def _get_kwargs(
    workspace_id: str,
    task_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/workspaces/{workspace_id}/tasks/{task_id}/stop".format(
            workspace_id=quote(str(workspace_id), safe=""),
            task_id=quote(str(task_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | StopTaskResponse | None:
    if response.status_code == 202:
        response_202 = StopTaskResponse.from_dict(response.json())

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
) -> Response[Error | StopTaskResponse]:
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
) -> Response[Error | StopTaskResponse]:
    """Stop a task

     Stops the task's running turn and returns `202` with `{"accepted": true}`. It works on any task in
    the workspace, whatever its source, and any member can stop one. A completed or cancelled task, or
    one whose session has already ended, is `409 not_running`.

    Args:
        workspace_id (str):
        task_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | StopTaskResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        task_id=task_id,
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
) -> Error | StopTaskResponse | None:
    """Stop a task

     Stops the task's running turn and returns `202` with `{"accepted": true}`. It works on any task in
    the workspace, whatever its source, and any member can stop one. A completed or cancelled task, or
    one whose session has already ended, is `409 not_running`.

    Args:
        workspace_id (str):
        task_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | StopTaskResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        task_id=task_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | StopTaskResponse]:
    """Stop a task

     Stops the task's running turn and returns `202` with `{"accepted": true}`. It works on any task in
    the workspace, whatever its source, and any member can stop one. A completed or cancelled task, or
    one whose session has already ended, is `409 not_running`.

    Args:
        workspace_id (str):
        task_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | StopTaskResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        task_id=task_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    task_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | StopTaskResponse | None:
    """Stop a task

     Stops the task's running turn and returns `202` with `{"accepted": true}`. It works on any task in
    the workspace, whatever its source, and any member can stop one. A completed or cancelled task, or
    one whose session has already ended, is `409 not_running`.

    Args:
        workspace_id (str):
        task_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | StopTaskResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            task_id=task_id,
            client=client,
        )
    ).parsed
