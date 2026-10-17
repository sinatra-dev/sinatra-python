"""When a request is retried, and how long the client waits first."""

from __future__ import annotations

import math
import time
from collections.abc import Callable
from datetime import UTC
from email.utils import parsedate_to_datetime

import httpx

MAX_RETRIES = 3
"""At most this many retries after the first attempt."""
BACKOFF_SECONDS = 0.5
"""The first ``503`` backoff; it doubles on each retry (0.5s, 1s, 2s)."""
MAX_RETRY_AFTER_SECONDS = 60.0
"""A ``Retry-After`` longer than this is cut to it."""

RETRY_IDEMPOTENT = frozenset({429, 503})
"""GETs, DELETE, and POSTs that carry an ``Idempotency-Key``."""
RETRY_UNAVAILABLE = frozenset({503})
"""``tasks.stop``: a stop is safe to repeat after a ``503``, but not after a ``429``."""
RETRY_NEVER: frozenset[int] = frozenset()
"""POSTs without an ``Idempotency-Key``: never retried."""

# The tests replace this with a fake clock.
sleep: Callable[[float], None] = time.sleep


def with_retries(retry_on: frozenset[int], attempt: Callable[[], httpx.Response]) -> httpx.Response:
    """Sends ``attempt()`` until it succeeds, fails with a status ``retry_on``
    doesn't cover, or runs out of retries, and returns the last response.

    Every attempt must send the same request: callers compute the
    ``Idempotency-Key`` once, outside ``attempt``. Exceptions (network errors,
    timeouts) are never retried.
    """
    retry = 0
    while True:
        response = attempt()
        if response.is_success or retry >= MAX_RETRIES or response.status_code not in retry_on:
            return response
        sleep(retry_delay(response, retry))
        retry += 1


def retry_delay(response: httpx.Response, retry: int) -> float:
    if response.status_code == 429:
        after = parse_retry_after(response.headers.get("retry-after"))
        if after is not None:
            return min(after, MAX_RETRY_AFTER_SECONDS)
    return float(BACKOFF_SECONDS * 2**retry)


def parse_retry_after(value: str | None) -> float | None:
    """``Retry-After`` is either seconds or an HTTP date. Returns seconds."""
    if value is None or not value.strip():
        return None
    try:
        seconds = float(value)
    except ValueError:
        pass
    else:
        return max(0.0, seconds) if math.isfinite(seconds) else None
    try:
        when = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:  # "-0000": HTTP dates are always GMT
        when = when.replace(tzinfo=UTC)
    return max(0.0, when.timestamp() - time.time())
