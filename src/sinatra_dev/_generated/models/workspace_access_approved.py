from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_access_approved_membership import (
        WorkspaceAccessApprovedMembership,
    )
    from ..models.workspace_access_approved_request import (
        WorkspaceAccessApprovedRequest,
    )


T = TypeVar("T", bound="WorkspaceAccessApproved")


@_attrs_define
class WorkspaceAccessApproved:
    """
    Attributes:
        request (WorkspaceAccessApprovedRequest):
        membership (WorkspaceAccessApprovedMembership):
    """

    request: WorkspaceAccessApprovedRequest
    membership: WorkspaceAccessApprovedMembership
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request = self.request.to_dict()

        membership = self.membership.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request": request,
                "membership": membership,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_access_approved_membership import (
            WorkspaceAccessApprovedMembership,
        )
        from ..models.workspace_access_approved_request import (
            WorkspaceAccessApprovedRequest,
        )

        d = dict(src_dict)
        request = WorkspaceAccessApprovedRequest.from_dict(d.pop("request"))

        membership = WorkspaceAccessApprovedMembership.from_dict(d.pop("membership"))

        workspace_access_approved = cls(
            request=request,
            membership=membership,
        )

        workspace_access_approved.additional_properties = d
        return workspace_access_approved

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
