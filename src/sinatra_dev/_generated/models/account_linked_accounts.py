from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_linked_accounts_telegram import AccountLinkedAccountsTelegram


T = TypeVar("T", bound="AccountLinkedAccounts")


@_attrs_define
class AccountLinkedAccounts:
    """
    Attributes:
        telegram (AccountLinkedAccountsTelegram): Telegram's dashboard-visible account state. Identity, routing and bot
            are null when unavailable.
    """

    telegram: AccountLinkedAccountsTelegram
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        telegram = self.telegram.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "telegram": telegram,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.account_linked_accounts_telegram import (
            AccountLinkedAccountsTelegram,
        )

        d = dict(src_dict)
        telegram = AccountLinkedAccountsTelegram.from_dict(d.pop("telegram"))

        account_linked_accounts = cls(
            telegram=telegram,
        )

        account_linked_accounts.additional_properties = d
        return account_linked_accounts

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
