from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_overview_linear_recent_teams_item import (
        WorkspaceOverviewLinearRecentTeamsItem,
    )


T = TypeVar("T", bound="WorkspaceOverviewLinear")


@_attrs_define
class WorkspaceOverviewLinear:
    """
    Attributes:
        status (str): `connected` or `not_connected`.
        organization_name (None | str):
        organization_url_key (None | str):
        current_user_has_read_token (bool):
        needs_reconnect (bool):
        recent_teams (list[WorkspaceOverviewLinearRecentTeamsItem]):
    """

    status: str
    organization_name: None | str
    organization_url_key: None | str
    current_user_has_read_token: bool
    needs_reconnect: bool
    recent_teams: list[WorkspaceOverviewLinearRecentTeamsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        organization_name: None | str
        organization_name = self.organization_name

        organization_url_key: None | str
        organization_url_key = self.organization_url_key

        current_user_has_read_token = self.current_user_has_read_token

        needs_reconnect = self.needs_reconnect

        recent_teams = []
        for recent_teams_item_data in self.recent_teams:
            recent_teams_item = recent_teams_item_data.to_dict()
            recent_teams.append(recent_teams_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "organizationName": organization_name,
                "organizationUrlKey": organization_url_key,
                "currentUserHasReadToken": current_user_has_read_token,
                "needsReconnect": needs_reconnect,
                "recentTeams": recent_teams,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_overview_linear_recent_teams_item import (
            WorkspaceOverviewLinearRecentTeamsItem,
        )

        d = dict(src_dict)
        status = d.pop("status")

        def _parse_organization_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        organization_name = _parse_organization_name(d.pop("organizationName"))

        def _parse_organization_url_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        organization_url_key = _parse_organization_url_key(d.pop("organizationUrlKey"))

        current_user_has_read_token = d.pop("currentUserHasReadToken")

        needs_reconnect = d.pop("needsReconnect")

        recent_teams = []
        _recent_teams = d.pop("recentTeams")
        for recent_teams_item_data in _recent_teams:
            recent_teams_item = WorkspaceOverviewLinearRecentTeamsItem.from_dict(
                recent_teams_item_data
            )

            recent_teams.append(recent_teams_item)

        workspace_overview_linear = cls(
            status=status,
            organization_name=organization_name,
            organization_url_key=organization_url_key,
            current_user_has_read_token=current_user_has_read_token,
            needs_reconnect=needs_reconnect,
            recent_teams=recent_teams,
        )

        workspace_overview_linear.additional_properties = d
        return workspace_overview_linear

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
