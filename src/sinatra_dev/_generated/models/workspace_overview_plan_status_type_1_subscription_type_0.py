from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkspaceOverviewPlanStatusType1SubscriptionType0")


@_attrs_define
class WorkspaceOverviewPlanStatusType1SubscriptionType0:
    """
    Attributes:
        status (str):
        current_period_end (datetime.datetime | None):
        trial_ends_at (datetime.datetime | None):
        past_due_since_at (datetime.datetime | None):
        cancel_at_period_end (bool):
        ends_at (datetime.datetime | None):
        action_required_hosted_invoice_url (None | str):
        capacity_plan (None | str):
    """

    status: str
    current_period_end: datetime.datetime | None
    trial_ends_at: datetime.datetime | None
    past_due_since_at: datetime.datetime | None
    cancel_at_period_end: bool
    ends_at: datetime.datetime | None
    action_required_hosted_invoice_url: None | str
    capacity_plan: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        current_period_end: None | str
        if isinstance(self.current_period_end, datetime.datetime):
            current_period_end = self.current_period_end.isoformat()
        else:
            current_period_end = self.current_period_end

        trial_ends_at: None | str
        if isinstance(self.trial_ends_at, datetime.datetime):
            trial_ends_at = self.trial_ends_at.isoformat()
        else:
            trial_ends_at = self.trial_ends_at

        past_due_since_at: None | str
        if isinstance(self.past_due_since_at, datetime.datetime):
            past_due_since_at = self.past_due_since_at.isoformat()
        else:
            past_due_since_at = self.past_due_since_at

        cancel_at_period_end = self.cancel_at_period_end

        ends_at: None | str
        if isinstance(self.ends_at, datetime.datetime):
            ends_at = self.ends_at.isoformat()
        else:
            ends_at = self.ends_at

        action_required_hosted_invoice_url: None | str
        action_required_hosted_invoice_url = self.action_required_hosted_invoice_url

        capacity_plan: None | str
        capacity_plan = self.capacity_plan

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "currentPeriodEnd": current_period_end,
                "trialEndsAt": trial_ends_at,
                "pastDueSinceAt": past_due_since_at,
                "cancelAtPeriodEnd": cancel_at_period_end,
                "endsAt": ends_at,
                "actionRequiredHostedInvoiceUrl": action_required_hosted_invoice_url,
                "capacityPlan": capacity_plan,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = d.pop("status")

        def _parse_current_period_end(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                current_period_end_type_0 = datetime.datetime.fromisoformat(data)

                return current_period_end_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        current_period_end = _parse_current_period_end(d.pop("currentPeriodEnd"))

        def _parse_trial_ends_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                trial_ends_at_type_0 = datetime.datetime.fromisoformat(data)

                return trial_ends_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        trial_ends_at = _parse_trial_ends_at(d.pop("trialEndsAt"))

        def _parse_past_due_since_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                past_due_since_at_type_0 = datetime.datetime.fromisoformat(data)

                return past_due_since_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        past_due_since_at = _parse_past_due_since_at(d.pop("pastDueSinceAt"))

        cancel_at_period_end = d.pop("cancelAtPeriodEnd")

        def _parse_ends_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ends_at_type_0 = datetime.datetime.fromisoformat(data)

                return ends_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        ends_at = _parse_ends_at(d.pop("endsAt"))

        def _parse_action_required_hosted_invoice_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        action_required_hosted_invoice_url = _parse_action_required_hosted_invoice_url(
            d.pop("actionRequiredHostedInvoiceUrl")
        )

        def _parse_capacity_plan(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        capacity_plan = _parse_capacity_plan(d.pop("capacityPlan"))

        workspace_overview_plan_status_type_1_subscription_type_0 = cls(
            status=status,
            current_period_end=current_period_end,
            trial_ends_at=trial_ends_at,
            past_due_since_at=past_due_since_at,
            cancel_at_period_end=cancel_at_period_end,
            ends_at=ends_at,
            action_required_hosted_invoice_url=action_required_hosted_invoice_url,
            capacity_plan=capacity_plan,
        )

        workspace_overview_plan_status_type_1_subscription_type_0.additional_properties = d
        return workspace_overview_plan_status_type_1_subscription_type_0

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
