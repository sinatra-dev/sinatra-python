from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_linked_accounts import AccountLinkedAccounts
    from ..models.account_memberships_item import AccountMembershipsItem
    from ..models.account_user import AccountUser


T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """Your own account, combining the dashboard's profile and linked accounts. The workspace path checks membership; the
    account belongs to the token's user, not the workspace owner.

        Attributes:
            user (AccountUser): Your dashboard-visible account identity. Credentials and session metadata are never
                returned.
            memberships (list[AccountMembershipsItem]): Your memberships and dashboard workspace summaries, ordered by
                workspace name.
            linked_accounts (AccountLinkedAccounts):
    """

    user: AccountUser
    memberships: list[AccountMembershipsItem]
    linked_accounts: AccountLinkedAccounts
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user = self.user.to_dict()

        memberships = []
        for memberships_item_data in self.memberships:
            memberships_item = memberships_item_data.to_dict()
            memberships.append(memberships_item)

        linked_accounts = self.linked_accounts.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
                "memberships": memberships,
                "linkedAccounts": linked_accounts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.account_linked_accounts import AccountLinkedAccounts
        from ..models.account_memberships_item import AccountMembershipsItem
        from ..models.account_user import AccountUser

        d = dict(src_dict)
        user = AccountUser.from_dict(d.pop("user"))

        memberships = []
        _memberships = d.pop("memberships")
        for memberships_item_data in _memberships:
            memberships_item = AccountMembershipsItem.from_dict(memberships_item_data)

            memberships.append(memberships_item)

        linked_accounts = AccountLinkedAccounts.from_dict(d.pop("linkedAccounts"))

        account = cls(
            user=user,
            memberships=memberships,
            linked_accounts=linked_accounts,
        )

        account.additional_properties = d
        return account

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
