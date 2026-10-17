"""The stub bodies come from openapi.json (spec_objects.py), so a field the API
newly requires can't break the wrapper tests or the release. These tests keep
the helper honest: whatever the spec says, it must produce objects the
generated models accept."""

from __future__ import annotations

import pytest
from spec_objects import component_names, spec_object

from sinatra_dev._generated import models

# Component schemas with a generated model of the same name (all but unions).
DECODABLE = [name for name in component_names() if hasattr(models, name)]


@pytest.mark.parametrize("name", DECODABLE)
def test_every_component_decodes_from_its_minimal_object(name: str) -> None:
    getattr(models, name).from_dict(spec_object(name))


def test_overrides_replace_only_what_they_name() -> None:
    task = spec_object("Task", status="teleporting", brandNewField=1)

    assert task["status"] == "teleporting"
    assert task["brandNewField"] == 1
    assert isinstance(task["id"], str)
    # Nullable (anyOf with null) fields are null in a minimal object.
    assert task["pullRequest"] is None


def test_an_unknown_component_is_an_error() -> None:
    with pytest.raises(KeyError, match="NoSuchSchema"):
        spec_object("NoSuchSchema")
