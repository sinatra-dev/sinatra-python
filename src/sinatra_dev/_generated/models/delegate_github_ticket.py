from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DelegateGithubTicket")


@_attrs_define
class DelegateGithubTicket:
    """A GitHub issue to delegate, by its repository and number.

    Attributes:
        source (Literal['github']): `github` to delegate a GitHub issue.
        repo (str): `owner/name` of a repository enabled in the workspace.
        number (int): The issue's number in that repository.
    """

    source: Literal["github"]
    repo: str
    number: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        repo = self.repo

        number = self.number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "repo": repo,
                "number": number,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        source = cast(Literal["github"], d.pop("source"))
        if source != "github":
            raise ValueError(f"source must match const 'github', got '{source}'")

        repo = d.pop("repo")

        number = d.pop("number")

        delegate_github_ticket = cls(
            source=source,
            repo=repo,
            number=number,
        )

        delegate_github_ticket.additional_properties = d
        return delegate_github_ticket

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
