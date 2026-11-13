from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.workspace_access_ok import WorkspaceAccessOk
from ...types import Response


def _get_kwargs(
    workspace_id: str,
    invite_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/workspaces/{workspace_id}/invites/{invite_id}".format(
            workspace_id=quote(str(workspace_id), safe=""),
            invite_id=quote(str(invite_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | WorkspaceAccessOk | None:
    if response.status_code == 200:
        response_200 = WorkspaceAccessOk.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 410:
        response_410 = Error.from_dict(response.json())

        return response_410

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | WorkspaceAccessOk]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | WorkspaceAccessOk]:
    """Revoke an invitation

     Owner only. Revokes an outstanding invitation in this workspace.

    Args:
        workspace_id (str):
        invite_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WorkspaceAccessOk]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        invite_id=invite_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | WorkspaceAccessOk | None:
    """Revoke an invitation

     Owner only. Revokes an outstanding invitation in this workspace.

    Args:
        workspace_id (str):
        invite_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WorkspaceAccessOk
    """

    return sync_detailed(
        workspace_id=workspace_id,
        invite_id=invite_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | WorkspaceAccessOk]:
    """Revoke an invitation

     Owner only. Revokes an outstanding invitation in this workspace.

    Args:
        workspace_id (str):
        invite_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WorkspaceAccessOk]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        invite_id=invite_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    invite_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | WorkspaceAccessOk | None:
    """Revoke an invitation

     Owner only. Revokes an outstanding invitation in this workspace.

    Args:
        workspace_id (str):
        invite_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WorkspaceAccessOk
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            invite_id=invite_id,
            client=client,
        )
    ).parsed
