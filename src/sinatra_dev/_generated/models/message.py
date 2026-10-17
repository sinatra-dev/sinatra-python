from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Message")


@_attrs_define
class Message:
    """An entry in a task's conversation.

    Attributes:
        id (str): The entry's id. Pass the last one you read as `after` to get only later entries.
        message_id (None | str): For a message a person sent: the id it was sent with, which is its idempotency key or a
            generated id. `null` on every other entry.
        role (str): Who wrote it: `user` for a person, `agent` for the agent, `platform` for Sinatra itself. New roles
            can appear.
        kind (str): What it is: `message` (a person's message), `response` (the agent's answer for a turn, or a notice
            from Sinatra such as a stop or files the agent produced), `clarify` (a question the agent needs answered to
            continue) or `error` (a refusal or failure from Sinatra). New kinds can appear.
        body (str): The text.
        created_at (datetime.datetime): When it was written.
    """

    id: str
    message_id: None | str
    role: str
    kind: str
    body: str
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        message_id: None | str
        message_id = self.message_id

        role = self.role

        kind = self.kind

        body = self.body

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "messageId": message_id,
                "role": role,
                "kind": kind,
                "body": body,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_message_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        message_id = _parse_message_id(d.pop("messageId"))

        role = d.pop("role")

        kind = d.pop("kind")

        body = d.pop("body")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        message = cls(
            id=id,
            message_id=message_id,
            role=role,
            kind=kind,
            body=body,
            created_at=created_at,
        )

        message.additional_properties = d
        return message

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
