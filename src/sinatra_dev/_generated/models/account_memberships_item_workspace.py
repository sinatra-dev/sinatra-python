from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountMembershipsItemWorkspace")


@_attrs_define
class AccountMembershipsItemWorkspace:
    """
    Attributes:
        id (str):
        name (str):
        created_at (datetime.datetime):
        github_account_login (None | str):
        github_account_type (None | str):
        linear_organization_name (None | str):
    """

    id: str
    name: str
    created_at: datetime.datetime
    github_account_login: None | str
    github_account_type: None | str
    linear_organization_name: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        created_at = self.created_at.isoformat()

        github_account_login: None | str
        github_account_login = self.github_account_login

        github_account_type: None | str
        github_account_type = self.github_account_type

        linear_organization_name: None | str
        linear_organization_name = self.linear_organization_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "createdAt": created_at,
                "githubAccountLogin": github_account_login,
                "githubAccountType": github_account_type,
                "linearOrganizationName": linear_organization_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        def _parse_github_account_login(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        github_account_login = _parse_github_account_login(d.pop("githubAccountLogin"))

        def _parse_github_account_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        github_account_type = _parse_github_account_type(d.pop("githubAccountType"))

        def _parse_linear_organization_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        linear_organization_name = _parse_linear_organization_name(
            d.pop("linearOrganizationName")
        )

        account_memberships_item_workspace = cls(
            id=id,
            name=name,
            created_at=created_at,
            github_account_login=github_account_login,
            github_account_type=github_account_type,
            linear_organization_name=linear_organization_name,
        )

        account_memberships_item_workspace.additional_properties = d
        return account_memberships_item_workspace

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
