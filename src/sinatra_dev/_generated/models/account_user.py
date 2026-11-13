from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountUser")


@_attrs_define
class AccountUser:
    """Your dashboard-visible account identity. Credentials and session metadata are never returned.

    Attributes:
        id (str):
        email (str):
        github_login (None | str):
        name (None | str):
        avatar_url (None | str):
        linear_user_id (None | str):
    """

    id: str
    email: str
    github_login: None | str
    name: None | str
    avatar_url: None | str
    linear_user_id: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        email = self.email

        github_login: None | str
        github_login = self.github_login

        name: None | str
        name = self.name

        avatar_url: None | str
        avatar_url = self.avatar_url

        linear_user_id: None | str
        linear_user_id = self.linear_user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "email": email,
                "githubLogin": github_login,
                "name": name,
                "avatarUrl": avatar_url,
                "linearUserId": linear_user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        email = d.pop("email")

        def _parse_github_login(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        github_login = _parse_github_login(d.pop("githubLogin"))

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        def _parse_avatar_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        avatar_url = _parse_avatar_url(d.pop("avatarUrl"))

        def _parse_linear_user_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        linear_user_id = _parse_linear_user_id(d.pop("linearUserId"))

        account_user = cls(
            id=id,
            email=email,
            github_login=github_login,
            name=name,
            avatar_url=avatar_url,
            linear_user_id=linear_user_id,
        )

        account_user.additional_properties = d
        return account_user

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
