from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_access_access_requests_item_requester import (
        WorkspaceAccessAccessRequestsItemRequester,
    )


T = TypeVar("T", bound="WorkspaceAccessAccessRequestsItem")


@_attrs_define
class WorkspaceAccessAccessRequestsItem:
    """
    Attributes:
        id (str):
        state (str):
        requested_at (datetime.datetime):
        reviewed_at (datetime.datetime | None):
        assigned_role (None | str):
        requester (WorkspaceAccessAccessRequestsItemRequester):
    """

    id: str
    state: str
    requested_at: datetime.datetime
    reviewed_at: datetime.datetime | None
    assigned_role: None | str
    requester: WorkspaceAccessAccessRequestsItemRequester
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        state = self.state

        requested_at = self.requested_at.isoformat()

        reviewed_at: None | str
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        assigned_role: None | str
        assigned_role = self.assigned_role

        requester = self.requester.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "state": state,
                "requestedAt": requested_at,
                "reviewedAt": reviewed_at,
                "assignedRole": assigned_role,
                "requester": requester,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_access_access_requests_item_requester import (
            WorkspaceAccessAccessRequestsItemRequester,
        )

        d = dict(src_dict)
        id = d.pop("id")

        state = d.pop("state")

        requested_at = datetime.datetime.fromisoformat(d.pop("requestedAt"))

        def _parse_reviewed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = datetime.datetime.fromisoformat(data)

                return reviewed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewedAt"))

        def _parse_assigned_role(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        assigned_role = _parse_assigned_role(d.pop("assignedRole"))

        requester = WorkspaceAccessAccessRequestsItemRequester.from_dict(
            d.pop("requester")
        )

        workspace_access_access_requests_item = cls(
            id=id,
            state=state,
            requested_at=requested_at,
            reviewed_at=reviewed_at,
            assigned_role=assigned_role,
            requester=requester,
        )

        workspace_access_access_requests_item.additional_properties = d
        return workspace_access_access_requests_item

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
