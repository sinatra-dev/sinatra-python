from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_linked_accounts_telegram_bot_type_0 import (
        AccountLinkedAccountsTelegramBotType0,
    )
    from ..models.account_linked_accounts_telegram_identity_type_0 import (
        AccountLinkedAccountsTelegramIdentityType0,
    )
    from ..models.account_linked_accounts_telegram_request_workspaces_type_0 import (
        AccountLinkedAccountsTelegramRequestWorkspacesType0,
    )


T = TypeVar("T", bound="AccountLinkedAccountsTelegram")


@_attrs_define
class AccountLinkedAccountsTelegram:
    """Telegram's dashboard-visible account state. Identity, routing and bot are null when unavailable.

    Attributes:
        available (bool):
        identity (AccountLinkedAccountsTelegramIdentityType0 | None):
        request_workspaces (AccountLinkedAccountsTelegramRequestWorkspacesType0 | None):
        bot (AccountLinkedAccountsTelegramBotType0 | None):
    """

    available: bool
    identity: AccountLinkedAccountsTelegramIdentityType0 | None
    request_workspaces: AccountLinkedAccountsTelegramRequestWorkspacesType0 | None
    bot: AccountLinkedAccountsTelegramBotType0 | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account_linked_accounts_telegram_bot_type_0 import (
            AccountLinkedAccountsTelegramBotType0,
        )
        from ..models.account_linked_accounts_telegram_identity_type_0 import (
            AccountLinkedAccountsTelegramIdentityType0,
        )
        from ..models.account_linked_accounts_telegram_request_workspaces_type_0 import (
            AccountLinkedAccountsTelegramRequestWorkspacesType0,
        )

        available = self.available

        identity: dict[str, Any] | None
        if isinstance(self.identity, AccountLinkedAccountsTelegramIdentityType0):
            identity = self.identity.to_dict()
        else:
            identity = self.identity

        request_workspaces: dict[str, Any] | None
        if isinstance(
            self.request_workspaces, AccountLinkedAccountsTelegramRequestWorkspacesType0
        ):
            request_workspaces = self.request_workspaces.to_dict()
        else:
            request_workspaces = self.request_workspaces

        bot: dict[str, Any] | None
        if isinstance(self.bot, AccountLinkedAccountsTelegramBotType0):
            bot = self.bot.to_dict()
        else:
            bot = self.bot

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available": available,
                "identity": identity,
                "requestWorkspaces": request_workspaces,
                "bot": bot,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.account_linked_accounts_telegram_bot_type_0 import (
            AccountLinkedAccountsTelegramBotType0,
        )
        from ..models.account_linked_accounts_telegram_identity_type_0 import (
            AccountLinkedAccountsTelegramIdentityType0,
        )
        from ..models.account_linked_accounts_telegram_request_workspaces_type_0 import (
            AccountLinkedAccountsTelegramRequestWorkspacesType0,
        )

        d = dict(src_dict)
        available = d.pop("available")

        def _parse_identity(
            data: object,
        ) -> AccountLinkedAccountsTelegramIdentityType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                identity_type_0 = AccountLinkedAccountsTelegramIdentityType0.from_dict(
                    data
                )

                return identity_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AccountLinkedAccountsTelegramIdentityType0 | None, data)

        identity = _parse_identity(d.pop("identity"))

        def _parse_request_workspaces(
            data: object,
        ) -> AccountLinkedAccountsTelegramRequestWorkspacesType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                request_workspaces_type_0 = (
                    AccountLinkedAccountsTelegramRequestWorkspacesType0.from_dict(data)
                )

                return request_workspaces_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                AccountLinkedAccountsTelegramRequestWorkspacesType0 | None, data
            )

        request_workspaces = _parse_request_workspaces(d.pop("requestWorkspaces"))

        def _parse_bot(data: object) -> AccountLinkedAccountsTelegramBotType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                bot_type_0 = AccountLinkedAccountsTelegramBotType0.from_dict(data)

                return bot_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AccountLinkedAccountsTelegramBotType0 | None, data)

        bot = _parse_bot(d.pop("bot"))

        account_linked_accounts_telegram = cls(
            available=available,
            identity=identity,
            request_workspaces=request_workspaces,
            bot=bot,
        )

        account_linked_accounts_telegram.additional_properties = d
        return account_linked_accounts_telegram

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
