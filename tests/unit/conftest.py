"""Fixtures for the wrapper tests: a stub server and a fake clock (see stub_server.py)."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from stub_server import FakeClock, Stub

from sinatra_dev import _retry


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> FakeClock:
    fake = FakeClock()
    monkeypatch.setattr(_retry, "sleep", fake.sleep)
    return fake


@pytest.fixture
def stub(clock: FakeClock) -> Iterator[Stub]:
    server = Stub(clock)
    yield server
    server.close()
