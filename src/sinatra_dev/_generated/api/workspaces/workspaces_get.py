from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.workspace_overview import WorkspaceOverview
from ...types import Response


def _get_kwargs(
    workspace_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/workspaces/{workspace_id}".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | WorkspaceOverview | None:
    if response.status_code == 200:
        response_200 = WorkspaceOverview.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

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
) -> Response[Error | WorkspaceOverview]:
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
) -> Response[Error | WorkspaceOverview]:
    """Get a workspace overview

     Returns the workspace's dashboard-visible integration state, connected repository catalog, plan
    status and saved model default, including your role and your own linked integration identity. Any
    current workspace member can read it. This is read-only: it doesn't reconcile repositories, refresh
    provider tokens or expose credentials. Unknown workspaces and workspaces you don't belong to both
    answer `404 not_found`.

    Args:
        workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WorkspaceOverview]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | WorkspaceOverview | None:
    """Get a workspace overview

     Returns the workspace's dashboard-visible integration state, connected repository catalog, plan
    status and saved model default, including your role and your own linked integration identity. Any
    current workspace member can read it. This is read-only: it doesn't reconcile repositories, refresh
    provider tokens or expose credentials. Unknown workspaces and workspaces you don't belong to both
    answer `404 not_found`.

    Args:
        workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WorkspaceOverview
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | WorkspaceOverview]:
    """Get a workspace overview

     Returns the workspace's dashboard-visible integration state, connected repository catalog, plan
    status and saved model default, including your role and your own linked integration identity. Any
    current workspace member can read it. This is read-only: it doesn't reconcile repositories, refresh
    provider tokens or expose credentials. Unknown workspaces and workspaces you don't belong to both
    answer `404 not_found`.

    Args:
        workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WorkspaceOverview]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | WorkspaceOverview | None:
    """Get a workspace overview

     Returns the workspace's dashboard-visible integration state, connected repository catalog, plan
    status and saved model default, including your role and your own linked integration identity. Any
    current workspace member can read it. This is read-only: it doesn't reconcile repositories, refresh
    provider tokens or expose credentials. Unknown workspaces and workspaces you don't belong to both
    answer `404 not_found`.

    Args:
        workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WorkspaceOverview
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
        )
    ).parsed
