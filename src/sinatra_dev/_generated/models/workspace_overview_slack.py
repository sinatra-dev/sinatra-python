from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_overview_slack_identity_type_0 import (
        WorkspaceOverviewSlackIdentityType0,
    )


T = TypeVar("T", bound="WorkspaceOverviewSlack")


@_attrs_define
class WorkspaceOverviewSlack:
    """
    Attributes:
        available (bool):
        status (str): `connected`, `inactive` or `not_connected`.
        team_name (None | str):
        allow_external_shared_channels (bool):
        identity (None | WorkspaceOverviewSlackIdentityType0):
    """

    available: bool
    status: str
    team_name: None | str
    allow_external_shared_channels: bool
    identity: None | WorkspaceOverviewSlackIdentityType0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.workspace_overview_slack_identity_type_0 import (
            WorkspaceOverviewSlackIdentityType0,
        )

        available = self.available

        status = self.status

        team_name: None | str
        team_name = self.team_name

        allow_external_shared_channels = self.allow_external_shared_channels

        identity: dict[str, Any] | None
        if isinstance(self.identity, WorkspaceOverviewSlackIdentityType0):
            identity = self.identity.to_dict()
        else:
            identity = self.identity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available": available,
                "status": status,
                "teamName": team_name,
                "allowExternalSharedChannels": allow_external_shared_channels,
                "identity": identity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_overview_slack_identity_type_0 import (
            WorkspaceOverviewSlackIdentityType0,
        )

        d = dict(src_dict)
        available = d.pop("available")

        status = d.pop("status")

        def _parse_team_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        team_name = _parse_team_name(d.pop("teamName"))

        allow_external_shared_channels = d.pop("allowExternalSharedChannels")

        def _parse_identity(data: object) -> None | WorkspaceOverviewSlackIdentityType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                identity_type_0 = WorkspaceOverviewSlackIdentityType0.from_dict(data)

                return identity_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | WorkspaceOverviewSlackIdentityType0, data)

        identity = _parse_identity(d.pop("identity"))

        workspace_overview_slack = cls(
            available=available,
            status=status,
            team_name=team_name,
            allow_external_shared_channels=allow_external_shared_channels,
            identity=identity,
        )

        workspace_overview_slack.additional_properties = d
        return workspace_overview_slack

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
