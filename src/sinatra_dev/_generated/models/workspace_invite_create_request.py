from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_invite_create_request_role import (
    WorkspaceInviteCreateRequestRole,
)

T = TypeVar("T", bound="WorkspaceInviteCreateRequest")


@_attrs_define
class WorkspaceInviteCreateRequest:
    """
    Attributes:
        email (str):
        role (WorkspaceInviteCreateRequestRole):
    """

    email: str
    role: WorkspaceInviteCreateRequestRole
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        email = d.pop("email")

        role = WorkspaceInviteCreateRequestRole(d.pop("role"))

        workspace_invite_create_request = cls(
            email=email,
            role=role,
        )

        workspace_invite_create_request.additional_properties = d
        return workspace_invite_create_request

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
