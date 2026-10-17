from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Ticket")


@_attrs_define
class Ticket:
    """An open issue you could delegate to Sinatra.

    Attributes:
        id (str): The issue's id on Sinatra's side. For GitHub it looks like `github:owner/name#42`.
        source (str): Where the issue lives: `linear` or `github`. New sources can appear.
        identifier (str): What to delegate it by. A Linear identifier such as `ENG-123` (send it as `id`), or a GitHub
            `owner/name#42` (send `owner/name` as `repo` and `42` as `number`).
        title (str): The issue's title.
        yours (bool): `true` if the issue is assigned to you or you wrote it.
        state (None | str): A GitHub issue's state, such as `open`. `null` for a Linear issue.
        context (None | str): The Linear team's name, or the GitHub repository's name.
        url (str): The issue's address on its tracker.
        workspace_id (str): The id of the workspace that was searched.
        workspace_label (str): The name the dashboard's ticket picker gives that workspace.
    """

    id: str
    source: str
    identifier: str
    title: str
    yours: bool
    state: None | str
    context: None | str
    url: str
    workspace_id: str
    workspace_label: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        source = self.source

        identifier = self.identifier

        title = self.title

        yours = self.yours

        state: None | str
        state = self.state

        context: None | str
        context = self.context

        url = self.url

        workspace_id = self.workspace_id

        workspace_label = self.workspace_label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "source": source,
                "identifier": identifier,
                "title": title,
                "yours": yours,
                "state": state,
                "context": context,
                "url": url,
                "workspaceId": workspace_id,
                "workspaceLabel": workspace_label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        source = d.pop("source")

        identifier = d.pop("identifier")

        title = d.pop("title")

        yours = d.pop("yours")

        def _parse_state(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        state = _parse_state(d.pop("state"))

        def _parse_context(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        context = _parse_context(d.pop("context"))

        url = d.pop("url")

        workspace_id = d.pop("workspaceId")

        workspace_label = d.pop("workspaceLabel")

        ticket = cls(
            id=id,
            source=source,
            identifier=identifier,
            title=title,
            yours=yours,
            state=state,
            context=context,
            url=url,
            workspace_id=workspace_id,
            workspace_label=workspace_label,
        )

        ticket.additional_properties = d
        return ticket

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
