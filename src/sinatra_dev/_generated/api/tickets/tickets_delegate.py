from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delegate_github_ticket import DelegateGithubTicket
from ...models.delegate_linear_ticket import DelegateLinearTicket
from ...models.delegate_ticket_response import DelegateTicketResponse
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    workspace_id: str,
    *,
    body: DelegateGithubTicket | DelegateLinearTicket,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/workspaces/{workspace_id}/tickets/delegate".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    if isinstance(body, DelegateLinearTicket):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DelegateTicketResponse | Error | None:
    if response.status_code == 202:
        response_202 = DelegateTicketResponse.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DelegateTicketResponse | Error]:
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
    body: DelegateGithubTicket | DelegateLinearTicket,
) -> Response[DelegateTicketResponse | Error]:
    """Delegate an issue

     Hands Sinatra an existing Linear or GitHub issue as you, as if you'd assigned it to Sinatra
    yourself, and returns `202` with `{"ok": true}`. The task then runs on the issue. Its conversation
    is there, not under Read the conversation, and it appears in List tasks once Sinatra picks it up.

    The rules match delegating from the dashboard. Sinatra reads a Linear issue as your linked Linear
    account, so you can only delegate issues you can see. Closed issues, pull requests and issues
    assigned to someone else are refused. If the workspace's queue is full, the request is refused
    before the issue is touched.

    A refusal returns an `error` code and a `reason` that says what to fix, for example `{"error":
    "linear_identity_unlinked", "reason": "Link your Linear identity in Settings first."}`.

    Args:
        workspace_id (str):
        body (DelegateGithubTicket | DelegateLinearTicket): An issue to delegate: a Linear issue
            by `id`, or a GitHub issue by `repo` and `number`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DelegateTicketResponse | Error]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DelegateGithubTicket | DelegateLinearTicket,
) -> DelegateTicketResponse | Error | None:
    """Delegate an issue

     Hands Sinatra an existing Linear or GitHub issue as you, as if you'd assigned it to Sinatra
    yourself, and returns `202` with `{"ok": true}`. The task then runs on the issue. Its conversation
    is there, not under Read the conversation, and it appears in List tasks once Sinatra picks it up.

    The rules match delegating from the dashboard. Sinatra reads a Linear issue as your linked Linear
    account, so you can only delegate issues you can see. Closed issues, pull requests and issues
    assigned to someone else are refused. If the workspace's queue is full, the request is refused
    before the issue is touched.

    A refusal returns an `error` code and a `reason` that says what to fix, for example `{"error":
    "linear_identity_unlinked", "reason": "Link your Linear identity in Settings first."}`.

    Args:
        workspace_id (str):
        body (DelegateGithubTicket | DelegateLinearTicket): An issue to delegate: a Linear issue
            by `id`, or a GitHub issue by `repo` and `number`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DelegateTicketResponse | Error
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DelegateGithubTicket | DelegateLinearTicket,
) -> Response[DelegateTicketResponse | Error]:
    """Delegate an issue

     Hands Sinatra an existing Linear or GitHub issue as you, as if you'd assigned it to Sinatra
    yourself, and returns `202` with `{"ok": true}`. The task then runs on the issue. Its conversation
    is there, not under Read the conversation, and it appears in List tasks once Sinatra picks it up.

    The rules match delegating from the dashboard. Sinatra reads a Linear issue as your linked Linear
    account, so you can only delegate issues you can see. Closed issues, pull requests and issues
    assigned to someone else are refused. If the workspace's queue is full, the request is refused
    before the issue is touched.

    A refusal returns an `error` code and a `reason` that says what to fix, for example `{"error":
    "linear_identity_unlinked", "reason": "Link your Linear identity in Settings first."}`.

    Args:
        workspace_id (str):
        body (DelegateGithubTicket | DelegateLinearTicket): An issue to delegate: a Linear issue
            by `id`, or a GitHub issue by `repo` and `number`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DelegateTicketResponse | Error]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DelegateGithubTicket | DelegateLinearTicket,
) -> DelegateTicketResponse | Error | None:
    """Delegate an issue

     Hands Sinatra an existing Linear or GitHub issue as you, as if you'd assigned it to Sinatra
    yourself, and returns `202` with `{"ok": true}`. The task then runs on the issue. Its conversation
    is there, not under Read the conversation, and it appears in List tasks once Sinatra picks it up.

    The rules match delegating from the dashboard. Sinatra reads a Linear issue as your linked Linear
    account, so you can only delegate issues you can see. Closed issues, pull requests and issues
    assigned to someone else are refused. If the workspace's queue is full, the request is refused
    before the issue is touched.

    A refusal returns an `error` code and a `reason` that says what to fix, for example `{"error":
    "linear_identity_unlinked", "reason": "Link your Linear identity in Settings first."}`.

    Args:
        workspace_id (str):
        body (DelegateGithubTicket | DelegateLinearTicket): An issue to delegate: a Linear issue
            by `id`, or a GitHub issue by `repo` and `number`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DelegateTicketResponse | Error
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
        )
    ).parsed
