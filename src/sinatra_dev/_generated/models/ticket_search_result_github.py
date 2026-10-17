from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TicketSearchResultGithub")


@_attrs_define
class TicketSearchResultGithub:
    """The workspace's GitHub connection.

    Attributes:
        connected (bool): Whether the workspace is connected to GitHub.
        repo (None | str): The repository the GitHub search covered, when the `repo` query matched an enabled one and
            had open issues. Otherwise `null`.
    """

    connected: bool
    repo: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connected = self.connected

        repo: None | str
        repo = self.repo

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connected": connected,
                "repo": repo,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        connected = d.pop("connected")

        def _parse_repo(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        repo = _parse_repo(d.pop("repo"))

        ticket_search_result_github = cls(
            connected=connected,
            repo=repo,
        )

        ticket_search_result_github.additional_properties = d
        return ticket_search_result_github

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
