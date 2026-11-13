from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_invite import WorkspaceInvite


T = TypeVar("T", bound="WorkspaceInviteResponse")


@_attrs_define
class WorkspaceInviteResponse:
    """
    Attributes:
        invite (WorkspaceInvite): An invitation's public metadata. No invitation token or redemption secret is returned.
    """

    invite: WorkspaceInvite
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        invite = self.invite.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "invite": invite,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_invite import WorkspaceInvite

        d = dict(src_dict)
        invite = WorkspaceInvite.from_dict(d.pop("invite"))

        workspace_invite_response = cls(
            invite=invite,
        )

        workspace_invite_response.additional_properties = d
        return workspace_invite_response

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
