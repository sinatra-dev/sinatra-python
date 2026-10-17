from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.ticket_search_result import TicketSearchResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: str,
    *,
    q: str | Unset = UNSET,
    repo: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    params["repo"] = repo

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/workspaces/{workspace_id}/tickets".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | TicketSearchResult | None:
    if response.status_code == 200:
        response_200 = TicketSearchResult.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | TicketSearchResult]:
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
    q: str | Unset = UNSET,
    repo: str | Unset = UNSET,
) -> Response[Error | TicketSearchResult]:
    """Search issues

     Lists the open Linear and GitHub issues you could delegate. It is the same list as the dashboard's
    ticket picker: yours first, then your team's unassigned ones, Linear's before GitHub's, at most 10
    from each tracker.

    Issues assigned to someone else, closed, or already being worked on are left out, and so are pull
    requests. Linear issues appear only when your Linear account is linked, and are read as you. GitHub
    issues appear only if you have a GitHub account, and only from the repositories enabled in the
    workspace.

    To delegate one, pass a Linear issue's `identifier` as `id`, or a GitHub issue's `identifier` split
    into `repo` and `number`.

    Args:
        workspace_id (str):
        q (str | Unset):
        repo (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TicketSearchResult]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        q=q,
        repo=repo,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = UNSET,
    repo: str | Unset = UNSET,
) -> Error | TicketSearchResult | None:
    """Search issues

     Lists the open Linear and GitHub issues you could delegate. It is the same list as the dashboard's
    ticket picker: yours first, then your team's unassigned ones, Linear's before GitHub's, at most 10
    from each tracker.

    Issues assigned to someone else, closed, or already being worked on are left out, and so are pull
    requests. Linear issues appear only when your Linear account is linked, and are read as you. GitHub
    issues appear only if you have a GitHub account, and only from the repositories enabled in the
    workspace.

    To delegate one, pass a Linear issue's `identifier` as `id`, or a GitHub issue's `identifier` split
    into `repo` and `number`.

    Args:
        workspace_id (str):
        q (str | Unset):
        repo (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TicketSearchResult
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        q=q,
        repo=repo,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = UNSET,
    repo: str | Unset = UNSET,
) -> Response[Error | TicketSearchResult]:
    """Search issues

     Lists the open Linear and GitHub issues you could delegate. It is the same list as the dashboard's
    ticket picker: yours first, then your team's unassigned ones, Linear's before GitHub's, at most 10
    from each tracker.

    Issues assigned to someone else, closed, or already being worked on are left out, and so are pull
    requests. Linear issues appear only when your Linear account is linked, and are read as you. GitHub
    issues appear only if you have a GitHub account, and only from the repositories enabled in the
    workspace.

    To delegate one, pass a Linear issue's `identifier` as `id`, or a GitHub issue's `identifier` split
    into `repo` and `number`.

    Args:
        workspace_id (str):
        q (str | Unset):
        repo (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TicketSearchResult]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        q=q,
        repo=repo,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = UNSET,
    repo: str | Unset = UNSET,
) -> Error | TicketSearchResult | None:
    """Search issues

     Lists the open Linear and GitHub issues you could delegate. It is the same list as the dashboard's
    ticket picker: yours first, then your team's unassigned ones, Linear's before GitHub's, at most 10
    from each tracker.

    Issues assigned to someone else, closed, or already being worked on are left out, and so are pull
    requests. Linear issues appear only when your Linear account is linked, and are read as you. GitHub
    issues appear only if you have a GitHub account, and only from the repositories enabled in the
    workspace.

    To delegate one, pass a Linear issue's `identifier` as `id`, or a GitHub issue's `identifier` split
    into `repo` and `number`.

    Args:
        workspace_id (str):
        q (str | Unset):
        repo (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TicketSearchResult
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            q=q,
            repo=repo,
        )
    ).parsed
