from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateEmailPreferencesRequestType0")


@_attrs_define
class UpdateEmailPreferencesRequestType0:
    """
    Attributes:
        setup_reminders (bool):
        task_alerts (bool | Unset):
    """

    setup_reminders: bool
    task_alerts: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        setup_reminders = self.setup_reminders

        task_alerts = self.task_alerts

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "setupReminders": setup_reminders,
            }
        )
        if task_alerts is not UNSET:
            field_dict["taskAlerts"] = task_alerts

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        setup_reminders = d.pop("setupReminders")

        task_alerts = d.pop("taskAlerts", UNSET)

        update_email_preferences_request_type_0 = cls(
            setup_reminders=setup_reminders,
            task_alerts=task_alerts,
        )

        return update_email_preferences_request_type_0
