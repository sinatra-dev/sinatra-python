from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.workspace_ownership_transferred import WorkspaceOwnershipTransferred
from ...types import Response


def _get_kwargs(
    workspace_id: str,
    membership_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/workspaces/{workspace_id}/memberships/{membership_id}/transfer".format(
            workspace_id=quote(str(workspace_id), safe=""),
            membership_id=quote(str(membership_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | WorkspaceOwnershipTransferred | None:
    if response.status_code == 200:
        response_200 = WorkspaceOwnershipTransferred.from_dict(response.json())

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
) -> Response[Error | WorkspaceOwnershipTransferred]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: str,
    membership_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | WorkspaceOwnershipTransferred]:
    """Transfer workspace ownership

     Owner only. Atomically promotes the target member to owner and demotes the caller to admin. The
    target must be a different non-owner member.

    Args:
        workspace_id (str):
        membership_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WorkspaceOwnershipTransferred]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        membership_id=membership_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    membership_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | WorkspaceOwnershipTransferred | None:
    """Transfer workspace ownership

     Owner only. Atomically promotes the target member to owner and demotes the caller to admin. The
    target must be a different non-owner member.

    Args:
        workspace_id (str):
        membership_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WorkspaceOwnershipTransferred
    """

    return sync_detailed(
        workspace_id=workspace_id,
        membership_id=membership_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    membership_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | WorkspaceOwnershipTransferred]:
    """Transfer workspace ownership

     Owner only. Atomically promotes the target member to owner and demotes the caller to admin. The
    target must be a different non-owner member.

    Args:
        workspace_id (str):
        membership_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WorkspaceOwnershipTransferred]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        membership_id=membership_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    membership_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | WorkspaceOwnershipTransferred | None:
    """Transfer workspace ownership

     Owner only. Atomically promotes the target member to owner and demotes the caller to admin. The
    target must be a different non-owner member.

    Args:
        workspace_id (str):
        membership_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WorkspaceOwnershipTransferred
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            membership_id=membership_id,
            client=client,
        )
    ).parsed
