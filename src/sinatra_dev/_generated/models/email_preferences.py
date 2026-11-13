from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EmailPreferences")


@_attrs_define
class EmailPreferences:
    """Your account-wide email preferences, shared with the signed email-preferences page.

    Attributes:
        setup_reminders (bool): Whether Sinatra may send you setup reminder emails.
        task_alerts (bool): Whether Sinatra may send you task alert emails.
    """

    setup_reminders: bool
    task_alerts: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        setup_reminders = self.setup_reminders

        task_alerts = self.task_alerts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "setupReminders": setup_reminders,
                "taskAlerts": task_alerts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        setup_reminders = d.pop("setupReminders")

        task_alerts = d.pop("taskAlerts")

        email_preferences = cls(
            setup_reminders=setup_reminders,
            task_alerts=task_alerts,
        )

        email_preferences.additional_properties = d
        return email_preferences

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
