from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.email_preferences import EmailPreferences
from ...models.error import Error
from ...models.update_email_preferences_request_type_0 import (
    UpdateEmailPreferencesRequestType0,
)
from ...models.update_email_preferences_request_type_1 import (
    UpdateEmailPreferencesRequestType1,
)
from ...types import Response


def _get_kwargs(
    *,
    body: UpdateEmailPreferencesRequestType0 | UpdateEmailPreferencesRequestType1,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/me/email-preferences",
    }

    if isinstance(body, UpdateEmailPreferencesRequestType0):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EmailPreferences | Error | None:
    if response.status_code == 200:
        response_200 = EmailPreferences.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

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
) -> Response[EmailPreferences | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: UpdateEmailPreferencesRequestType0 | UpdateEmailPreferencesRequestType1,
) -> Response[EmailPreferences | Error]:
    """Change your email preferences

     Sets at least one of setupReminders or taskAlerts, as JSON booleans. Omitted categories stay
    unchanged. true subscribes and false opts out. No workspace membership is required. Only the token
    user's preferences can be changed. The signed email-preferences page reads and writes the same
    settings.

    Args:
        body (UpdateEmailPreferencesRequestType0 | UpdateEmailPreferencesRequestType1): Set at
            least one boolean. Omitted categories are unchanged; these preferences belong to you
            across all your workspaces.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailPreferences | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: UpdateEmailPreferencesRequestType0 | UpdateEmailPreferencesRequestType1,
) -> EmailPreferences | Error | None:
    """Change your email preferences

     Sets at least one of setupReminders or taskAlerts, as JSON booleans. Omitted categories stay
    unchanged. true subscribes and false opts out. No workspace membership is required. Only the token
    user's preferences can be changed. The signed email-preferences page reads and writes the same
    settings.

    Args:
        body (UpdateEmailPreferencesRequestType0 | UpdateEmailPreferencesRequestType1): Set at
            least one boolean. Omitted categories are unchanged; these preferences belong to you
            across all your workspaces.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailPreferences | Error
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: UpdateEmailPreferencesRequestType0 | UpdateEmailPreferencesRequestType1,
) -> Response[EmailPreferences | Error]:
    """Change your email preferences

     Sets at least one of setupReminders or taskAlerts, as JSON booleans. Omitted categories stay
    unchanged. true subscribes and false opts out. No workspace membership is required. Only the token
    user's preferences can be changed. The signed email-preferences page reads and writes the same
    settings.

    Args:
        body (UpdateEmailPreferencesRequestType0 | UpdateEmailPreferencesRequestType1): Set at
            least one boolean. Omitted categories are unchanged; these preferences belong to you
            across all your workspaces.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailPreferences | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: UpdateEmailPreferencesRequestType0 | UpdateEmailPreferencesRequestType1,
) -> EmailPreferences | Error | None:
    """Change your email preferences

     Sets at least one of setupReminders or taskAlerts, as JSON booleans. Omitted categories stay
    unchanged. true subscribes and false opts out. No workspace membership is required. Only the token
    user's preferences can be changed. The signed email-preferences page reads and writes the same
    settings.

    Args:
        body (UpdateEmailPreferencesRequestType0 | UpdateEmailPreferencesRequestType1): Set at
            least one boolean. Omitted categories are unchanged; these preferences belong to you
            across all your workspaces.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailPreferences | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
