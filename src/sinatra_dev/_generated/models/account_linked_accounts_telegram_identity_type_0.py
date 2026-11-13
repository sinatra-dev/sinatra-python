from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountLinkedAccountsTelegramIdentityType0")


@_attrs_define
class AccountLinkedAccountsTelegramIdentityType0:
    """
    Attributes:
        telegram_user_id (str):
        display_name (None | str):
        linked_at (datetime.datetime):
    """

    telegram_user_id: str
    display_name: None | str
    linked_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        telegram_user_id = self.telegram_user_id

        display_name: None | str
        display_name = self.display_name

        linked_at = self.linked_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "telegramUserId": telegram_user_id,
                "displayName": display_name,
                "linkedAt": linked_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        telegram_user_id = d.pop("telegramUserId")

        def _parse_display_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        display_name = _parse_display_name(d.pop("displayName"))

        linked_at = datetime.datetime.fromisoformat(d.pop("linkedAt"))

        account_linked_accounts_telegram_identity_type_0 = cls(
            telegram_user_id=telegram_user_id,
            display_name=display_name,
            linked_at=linked_at,
        )

        account_linked_accounts_telegram_identity_type_0.additional_properties = d
        return account_linked_accounts_telegram_identity_type_0

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
