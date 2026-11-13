from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar(
    "T", bound="AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0"
)


@_attrs_define
class AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0:
    """
    Attributes:
        id (str):
        name (None | str):
        usable (bool):
    """

    id: str
    name: None | str
    usable: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name: None | str
        name = self.name

        usable = self.usable

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "usable": usable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        usable = d.pop("usable")

        account_linked_accounts_telegram_request_workspaces_type_0_current_type_0 = cls(
            id=id,
            name=name,
            usable=usable,
        )

        account_linked_accounts_telegram_request_workspaces_type_0_current_type_0.additional_properties = d
        return account_linked_accounts_telegram_request_workspaces_type_0_current_type_0

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
