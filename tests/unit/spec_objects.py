"""Minimal valid JSON objects for the spec's component schemas, built from the
committed openapi.json.

    spec_object("Task", status="teleporting")

fills every required property with a type-appropriate value and leaves the
optional ones out; keyword arguments (wire names, such as ``nextCursor``)
replace or add top-level fields. Stub bodies built this way keep up with the
spec on their own: when the API starts requiring a new field, the stubs carry
it, so only a real incompatibility (the drift check, the contract tests, the
wrapper's own typecheck) can fail the release.

Standard library only: scripts/smoke.py uses it from a venv that has nothing
but the built wheel.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any

SPEC = Path(__file__).resolve().parents[2] / "openapi.json"
DATE_TIME = "2026-10-16T12:00:00.000Z"


@cache
def _spec() -> dict[str, Any]:
    spec: dict[str, Any] = json.loads(SPEC.read_text())
    return spec


def component_names() -> list[str]:
    return sorted(_spec()["components"]["schemas"])


def spec_object(name: str, **overrides: Any) -> dict[str, Any]:
    """A minimal valid object for ``#/components/schemas/<name>``, with ``overrides`` on top."""
    schemas = _spec()["components"]["schemas"]
    if name not in schemas:
        raise KeyError(f"openapi.json has no component schema {name!r}")
    value = _minimal(schemas[name])
    if not isinstance(value, dict):
        raise TypeError(f"component {name!r} isn't an object schema")
    return {**value, **overrides}


def _resolve(ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"only local $refs are supported, not {ref!r}")
    node: Any = _spec()
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    resolved: dict[str, Any] = node
    return resolved


def _is_null(schema: dict[str, Any]) -> bool:
    return schema.get("type") == "null"


def _minimal(schema: dict[str, Any]) -> Any:
    if "$ref" in schema:
        return _minimal(_resolve(schema["$ref"]))
    if "const" in schema:
        return schema["const"]
    if "enum" in schema:
        return schema["enum"][0]
    for key in ("anyOf", "oneOf"):
        if key in schema:
            options: list[dict[str, Any]] = schema[key]
            # Nullable: the minimal value is null.
            if any(_is_null(option) for option in options):
                return None
            return _minimal(options[0])
    if "allOf" in schema:
        merged: dict[str, Any] = {}
        for part in schema["allOf"]:
            merged.update(_minimal(part))
        return merged
    if schema.get("nullable") is True:  # OpenAPI 3.0 style
        return None

    kind = schema.get("type")
    if isinstance(kind, list):  # OpenAPI 3.1: type: ["string", "null"]
        if "null" in kind:
            return None
        kind = kind[0]
    if kind == "object" or (kind is None and "properties" in schema):
        properties: dict[str, dict[str, Any]] = schema.get("properties", {})
        return {prop: _minimal(properties.get(prop, {})) for prop in schema.get("required", [])}
    if kind == "array":
        return [_minimal(schema.get("items", {})) for _ in range(schema.get("minItems", 0))]
    if kind == "string":
        if schema.get("format") == "date-time":
            return DATE_TIME
        if schema.get("format") in ("uri", "url"):
            return "https://example.com"
        return "x" * max(1, schema.get("minLength", 1))
    if kind == "integer":
        return _number(schema, 1)
    if kind == "number":
        return float(_number(schema, 1))
    if kind == "boolean":
        return False
    if kind == "null":
        return None
    # No type at all: any value is valid.
    return "x"


def _number(schema: dict[str, Any], step: int) -> int:
    if "minimum" in schema:
        return int(schema["minimum"])
    if "exclusiveMinimum" in schema and not isinstance(schema["exclusiveMinimum"], bool):
        return int(schema["exclusiveMinimum"]) + step
    return 0
