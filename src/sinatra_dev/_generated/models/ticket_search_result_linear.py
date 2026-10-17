from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TicketSearchResultLinear")


@_attrs_define
class TicketSearchResultLinear:
    """The workspace's Linear connection, as it applies to you.

    Attributes:
        connected (bool): Whether the workspace is connected to Linear.
        identity_linked (bool): Whether your Linear account is linked in this workspace. Linear issues are listed only
            when it is.
        identity_bound (bool): Whether your Linear identity is tied to your Sinatra user.
    """

    connected: bool
    identity_linked: bool
    identity_bound: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connected = self.connected

        identity_linked = self.identity_linked

        identity_bound = self.identity_bound

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connected": connected,
                "identityLinked": identity_linked,
                "identityBound": identity_bound,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        connected = d.pop("connected")

        identity_linked = d.pop("identityLinked")

        identity_bound = d.pop("identityBound")

        ticket_search_result_linear = cls(
            connected=connected,
            identity_linked=identity_linked,
            identity_bound=identity_bound,
        )

        ticket_search_result_linear.additional_properties = d
        return ticket_search_result_linear

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
