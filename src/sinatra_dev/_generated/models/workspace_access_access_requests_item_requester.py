from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkspaceAccessAccessRequestsItemRequester")


@_attrs_define
class WorkspaceAccessAccessRequestsItemRequester:
    """
    Attributes:
        id (str):
        name (None | str):
        github_login (None | str):
        avatar_url (None | str):
    """

    id: str
    name: None | str
    github_login: None | str
    avatar_url: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name: None | str
        name = self.name

        github_login: None | str
        github_login = self.github_login

        avatar_url: None | str
        avatar_url = self.avatar_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "githubLogin": github_login,
                "avatarUrl": avatar_url,
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

        def _parse_github_login(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        github_login = _parse_github_login(d.pop("githubLogin"))

        def _parse_avatar_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        avatar_url = _parse_avatar_url(d.pop("avatarUrl"))

        workspace_access_access_requests_item_requester = cls(
            id=id,
            name=name,
            github_login=github_login,
            avatar_url=avatar_url,
        )

        workspace_access_access_requests_item_requester.additional_properties = d
        return workspace_access_access_requests_item_requester

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
