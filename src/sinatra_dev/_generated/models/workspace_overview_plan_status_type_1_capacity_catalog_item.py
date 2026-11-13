from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkspaceOverviewPlanStatusType1CapacityCatalogItem")


@_attrs_define
class WorkspaceOverviewPlanStatusType1CapacityCatalogItem:
    """
    Attributes:
        plan (str):
        running (int):
        queued (int):
        price_usd (float):
    """

    plan: str
    running: int
    queued: int
    price_usd: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan = self.plan

        running = self.running

        queued = self.queued

        price_usd = self.price_usd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan": plan,
                "running": running,
                "queued": queued,
                "priceUsd": price_usd,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        plan = d.pop("plan")

        running = d.pop("running")

        queued = d.pop("queued")

        price_usd = d.pop("priceUsd")

        workspace_overview_plan_status_type_1_capacity_catalog_item = cls(
            plan=plan,
            running=running,
            queued=queued,
            price_usd=price_usd,
        )

        workspace_overview_plan_status_type_1_capacity_catalog_item.additional_properties = d
        return workspace_overview_plan_status_type_1_capacity_catalog_item

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
