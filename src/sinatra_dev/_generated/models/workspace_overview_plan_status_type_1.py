from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_overview_plan_status_type_1_capacity import (
        WorkspaceOverviewPlanStatusType1Capacity,
    )
    from ..models.workspace_overview_plan_status_type_1_capacity_catalog_item import (
        WorkspaceOverviewPlanStatusType1CapacityCatalogItem,
    )
    from ..models.workspace_overview_plan_status_type_1_subscription_type_0 import (
        WorkspaceOverviewPlanStatusType1SubscriptionType0,
    )


T = TypeVar("T", bound="WorkspaceOverviewPlanStatusType1")


@_attrs_define
class WorkspaceOverviewPlanStatusType1:
    """
    Attributes:
        plan (Literal['monthly']):
        byok_configured (bool): Whether your model credentials or a workspace key are configured.
        capacity (WorkspaceOverviewPlanStatusType1Capacity):
        capacity_catalog (list[WorkspaceOverviewPlanStatusType1CapacityCatalogItem]):
        subscription (None | WorkspaceOverviewPlanStatusType1SubscriptionType0):
    """

    plan: Literal["monthly"]
    byok_configured: bool
    capacity: WorkspaceOverviewPlanStatusType1Capacity
    capacity_catalog: list[WorkspaceOverviewPlanStatusType1CapacityCatalogItem]
    subscription: None | WorkspaceOverviewPlanStatusType1SubscriptionType0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.workspace_overview_plan_status_type_1_subscription_type_0 import (
            WorkspaceOverviewPlanStatusType1SubscriptionType0,
        )

        plan = self.plan

        byok_configured = self.byok_configured

        capacity = self.capacity.to_dict()

        capacity_catalog = []
        for capacity_catalog_item_data in self.capacity_catalog:
            capacity_catalog_item = capacity_catalog_item_data.to_dict()
            capacity_catalog.append(capacity_catalog_item)

        subscription: dict[str, Any] | None
        if isinstance(
            self.subscription, WorkspaceOverviewPlanStatusType1SubscriptionType0
        ):
            subscription = self.subscription.to_dict()
        else:
            subscription = self.subscription

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan": plan,
                "byokConfigured": byok_configured,
                "capacity": capacity,
                "capacityCatalog": capacity_catalog,
                "subscription": subscription,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_overview_plan_status_type_1_capacity import (
            WorkspaceOverviewPlanStatusType1Capacity,
        )
        from ..models.workspace_overview_plan_status_type_1_capacity_catalog_item import (
            WorkspaceOverviewPlanStatusType1CapacityCatalogItem,
        )
        from ..models.workspace_overview_plan_status_type_1_subscription_type_0 import (
            WorkspaceOverviewPlanStatusType1SubscriptionType0,
        )

        d = dict(src_dict)
        plan = cast(Literal["monthly"], d.pop("plan"))
        if plan != "monthly":
            raise ValueError(f"plan must match const 'monthly', got '{plan}'")

        byok_configured = d.pop("byokConfigured")

        capacity = WorkspaceOverviewPlanStatusType1Capacity.from_dict(d.pop("capacity"))

        capacity_catalog = []
        _capacity_catalog = d.pop("capacityCatalog")
        for capacity_catalog_item_data in _capacity_catalog:
            capacity_catalog_item = (
                WorkspaceOverviewPlanStatusType1CapacityCatalogItem.from_dict(
                    capacity_catalog_item_data
                )
            )

            capacity_catalog.append(capacity_catalog_item)

        def _parse_subscription(
            data: object,
        ) -> None | WorkspaceOverviewPlanStatusType1SubscriptionType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                subscription_type_0 = (
                    WorkspaceOverviewPlanStatusType1SubscriptionType0.from_dict(data)
                )

                return subscription_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | WorkspaceOverviewPlanStatusType1SubscriptionType0, data)

        subscription = _parse_subscription(d.pop("subscription"))

        workspace_overview_plan_status_type_1 = cls(
            plan=plan,
            byok_configured=byok_configured,
            capacity=capacity,
            capacity_catalog=capacity_catalog,
            subscription=subscription,
        )

        workspace_overview_plan_status_type_1.additional_properties = d
        return workspace_overview_plan_status_type_1

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
