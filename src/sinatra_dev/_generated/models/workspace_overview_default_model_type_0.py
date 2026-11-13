from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceOverviewDefaultModelType0")


@_attrs_define
class WorkspaceOverviewDefaultModelType0:
    """
    Attributes:
        engine (str):
        model (str):
        effort (str | Unset):
    """

    engine: str
    model: str
    effort: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        engine = self.engine

        model = self.model

        effort = self.effort

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "engine": engine,
                "model": model,
            }
        )
        if effort is not UNSET:
            field_dict["effort"] = effort

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        engine = d.pop("engine")

        model = d.pop("model")

        effort = d.pop("effort", UNSET)

        workspace_overview_default_model_type_0 = cls(
            engine=engine,
            model=model,
            effort=effort,
        )

        workspace_overview_default_model_type_0.additional_properties = d
        return workspace_overview_default_model_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
