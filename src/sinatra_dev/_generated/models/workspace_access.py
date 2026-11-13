from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_access_access_requests_item import (
        WorkspaceAccessAccessRequestsItem,
    )
    from ..models.workspace_access_memberships_item import (
        WorkspaceAccessMembershipsItem,
    )
    from ..models.workspace_invite import WorkspaceInvite


T = TypeVar("T", bound="WorkspaceAccess")


@_attrs_define
class WorkspaceAccess:
    """
    Attributes:
        memberships (list[WorkspaceAccessMembershipsItem]):
        access_requests (list[WorkspaceAccessAccessRequestsItem]):
        invites (list[WorkspaceInvite]):
    """

    memberships: list[WorkspaceAccessMembershipsItem]
    access_requests: list[WorkspaceAccessAccessRequestsItem]
    invites: list[WorkspaceInvite]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        memberships = []
        for memberships_item_data in self.memberships:
            memberships_item = memberships_item_data.to_dict()
            memberships.append(memberships_item)

        access_requests = []
        for access_requests_item_data in self.access_requests:
            access_requests_item = access_requests_item_data.to_dict()
            access_requests.append(access_requests_item)

        invites = []
        for invites_item_data in self.invites:
            invites_item = invites_item_data.to_dict()
            invites.append(invites_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "memberships": memberships,
                "accessRequests": access_requests,
                "invites": invites,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_access_access_requests_item import (
            WorkspaceAccessAccessRequestsItem,
        )
        from ..models.workspace_access_memberships_item import (
            WorkspaceAccessMembershipsItem,
        )
        from ..models.workspace_invite import WorkspaceInvite

        d = dict(src_dict)
        memberships = []
        _memberships = d.pop("memberships")
        for memberships_item_data in _memberships:
            memberships_item = WorkspaceAccessMembershipsItem.from_dict(
                memberships_item_data
            )

            memberships.append(memberships_item)

        access_requests = []
        _access_requests = d.pop("accessRequests")
        for access_requests_item_data in _access_requests:
            access_requests_item = WorkspaceAccessAccessRequestsItem.from_dict(
                access_requests_item_data
            )

            access_requests.append(access_requests_item)

        invites = []
        _invites = d.pop("invites")
        for invites_item_data in _invites:
            invites_item = WorkspaceInvite.from_dict(invites_item_data)

            invites.append(invites_item)

        workspace_access = cls(
            memberships=memberships,
            access_requests=access_requests,
            invites=invites,
        )

        workspace_access.additional_properties = d
        return workspace_access

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
