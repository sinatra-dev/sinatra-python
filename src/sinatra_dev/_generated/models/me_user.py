from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MeUser")


@_attrs_define
class MeUser:
    """The user the token acts as.

    Attributes:
        id (str): The user's id.
        github_login (None | str): The user's GitHub login. `null` for a user without GitHub.
        name (None | str): The user's name, if they have one.
    """

    id: str
    github_login: None | str
    name: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        github_login: None | str
        github_login = self.github_login

        name: None | str
        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "githubLogin": github_login,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

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

        me_user = cls(
            id=id,
            github_login=github_login,
            name=name,
        )

        me_user.additional_properties = d
        return me_user

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
