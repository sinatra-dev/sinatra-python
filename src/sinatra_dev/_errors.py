from __future__ import annotations

from typing import Any

import httpx


class SinatraError(Exception):
    """The one error the client raises for an HTTP error response.

    ``code`` is the API's machine-readable ``error`` code, such as
    ``capacity_full``. New codes can appear at any time, so treat it as an open
    string. Branch on ``code``, not on ``reason`` or the message.

    Network failures and timeouts are not wrapped: they raise the
    ``httpx.HTTPError`` that httpx raised.
    """

    status: int
    """The HTTP status, such as ``409``."""
    code: str
    """The API's ``error`` code, such as ``not_running``. ``http_error`` when the
    response had no code, for example an HTML page from a proxy."""
    reason: str | None
    """A sentence saying what went wrong, written to show to a person."""
    request_id: str | None
    """The request's id, from the body or the ``x-request-id`` header. Share it with support."""
    body: Any
    """The response body: the parsed JSON, or the text when it wasn't JSON."""
    headers: httpx.Headers
    """The response headers."""

    def __init__(self, status: int, body: Any, headers: httpx.Headers) -> None:
        fields: dict[str, Any] = body if isinstance(body, dict) else {}
        error = fields.get("error")
        reason = fields.get("reason")
        request_id = fields.get("requestId")
        self.status = status
        self.code = error if isinstance(error, str) else "http_error"
        self.reason = reason if isinstance(reason, str) else None
        self.request_id = request_id if isinstance(request_id, str) else headers.get("x-request-id")
        self.body = body
        self.headers = headers
        super().__init__(f"{status} {self.code}: {self.reason}" if self.reason else f"{status} {self.code}")

    @classmethod
    def from_response(cls, response: httpx.Response) -> SinatraError:
        body: Any
        try:
            body = response.json()
        except ValueError:
            body = response.text
        return cls(response.status_code, body, response.headers)
