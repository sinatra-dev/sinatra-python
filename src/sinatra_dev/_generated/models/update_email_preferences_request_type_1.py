from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateEmailPreferencesRequestType1")


@_attrs_define
class UpdateEmailPreferencesRequestType1:
    """
    Attributes:
        task_alerts (bool):
        setup_reminders (bool | Unset):
    """

    task_alerts: bool
    setup_reminders: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        task_alerts = self.task_alerts

        setup_reminders = self.setup_reminders

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "taskAlerts": task_alerts,
            }
        )
        if setup_reminders is not UNSET:
            field_dict["setupReminders"] = setup_reminders

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        task_alerts = d.pop("taskAlerts")

        setup_reminders = d.pop("setupReminders", UNSET)

        update_email_preferences_request_type_1 = cls(
            task_alerts=task_alerts,
            setup_reminders=setup_reminders,
        )

        return update_email_preferences_request_type_1
