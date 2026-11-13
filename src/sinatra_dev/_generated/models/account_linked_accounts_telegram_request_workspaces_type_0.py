from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_linked_accounts_telegram_request_workspaces_type_0_current_type_0 import (
        AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0,
    )
    from ..models.account_linked_accounts_telegram_request_workspaces_type_0_options_item import (
        AccountLinkedAccountsTelegramRequestWorkspacesType0OptionsItem,
    )
    from ..models.account_linked_accounts_telegram_request_workspaces_type_0_routes_to_type_0 import (
        AccountLinkedAccountsTelegramRequestWorkspacesType0RoutesToType0,
    )


T = TypeVar("T", bound="AccountLinkedAccountsTelegramRequestWorkspacesType0")


@_attrs_define
class AccountLinkedAccountsTelegramRequestWorkspacesType0:
    """
    Attributes:
        options (list[AccountLinkedAccountsTelegramRequestWorkspacesType0OptionsItem]):
        current (AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0 | None):
        routes_to (AccountLinkedAccountsTelegramRequestWorkspacesType0RoutesToType0 | None):
    """

    options: list[AccountLinkedAccountsTelegramRequestWorkspacesType0OptionsItem]
    current: AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0 | None
    routes_to: AccountLinkedAccountsTelegramRequestWorkspacesType0RoutesToType0 | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account_linked_accounts_telegram_request_workspaces_type_0_current_type_0 import (
            AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0,
        )
        from ..models.account_linked_accounts_telegram_request_workspaces_type_0_routes_to_type_0 import (
            AccountLinkedAccountsTelegramRequestWorkspacesType0RoutesToType0,
        )

        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()
            options.append(options_item)

        current: dict[str, Any] | None
        if isinstance(
            self.current,
            AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0,
        ):
            current = self.current.to_dict()
        else:
            current = self.current

        routes_to: dict[str, Any] | None
        if isinstance(
            self.routes_to,
            AccountLinkedAccountsTelegramRequestWorkspacesType0RoutesToType0,
        ):
            routes_to = self.routes_to.to_dict()
        else:
            routes_to = self.routes_to

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "options": options,
                "current": current,
                "routesTo": routes_to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.account_linked_accounts_telegram_request_workspaces_type_0_current_type_0 import (
            AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0,
        )
        from ..models.account_linked_accounts_telegram_request_workspaces_type_0_options_item import (
            AccountLinkedAccountsTelegramRequestWorkspacesType0OptionsItem,
        )
        from ..models.account_linked_accounts_telegram_request_workspaces_type_0_routes_to_type_0 import (
            AccountLinkedAccountsTelegramRequestWorkspacesType0RoutesToType0,
        )

        d = dict(src_dict)
        options = []
        _options = d.pop("options")
        for options_item_data in _options:
            options_item = AccountLinkedAccountsTelegramRequestWorkspacesType0OptionsItem.from_dict(
                options_item_data
            )

            options.append(options_item)

        def _parse_current(
            data: object,
        ) -> AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                current_type_0 = AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0.from_dict(
                    data
                )

                return current_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                AccountLinkedAccountsTelegramRequestWorkspacesType0CurrentType0 | None,
                data,
            )

        current = _parse_current(d.pop("current"))

        def _parse_routes_to(
            data: object,
        ) -> AccountLinkedAccountsTelegramRequestWorkspacesType0RoutesToType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                routes_to_type_0 = AccountLinkedAccountsTelegramRequestWorkspacesType0RoutesToType0.from_dict(
                    data
                )

                return routes_to_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                AccountLinkedAccountsTelegramRequestWorkspacesType0RoutesToType0 | None,
                data,
            )

        routes_to = _parse_routes_to(d.pop("routesTo"))

        account_linked_accounts_telegram_request_workspaces_type_0 = cls(
            options=options,
            current=current,
            routes_to=routes_to,
        )

        account_linked_accounts_telegram_request_workspaces_type_0.additional_properties = d
        return account_linked_accounts_telegram_request_workspaces_type_0

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
