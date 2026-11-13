from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkspaceOverviewPlanStatusType0")


@_attrs_define
class WorkspaceOverviewPlanStatusType0:
    """
    Attributes:
        plan (Literal['enterprise']):
    """

    plan: Literal["enterprise"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan = self.plan

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan": plan,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        plan = cast(Literal["enterprise"], d.pop("plan"))
        if plan != "enterprise":
            raise ValueError(f"plan must match const 'enterprise', got '{plan}'")

        workspace_overview_plan_status_type_0 = cls(
            plan=plan,
        )

        workspace_overview_plan_status_type_0.additional_properties = d
        return workspace_overview_plan_status_type_0

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
