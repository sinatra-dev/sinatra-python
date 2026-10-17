from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.me_user import MeUser
    from ..models.workspace import Workspace


T = TypeVar("T", bound="Me")


@_attrs_define
class Me:
    """The token's user and workspaces.

    Attributes:
        user (MeUser): The user the token acts as.
        workspaces (list[Workspace]): The workspaces the user belongs to, ordered by name.
    """

    user: MeUser
    workspaces: list[Workspace]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user = self.user.to_dict()

        workspaces = []
        for workspaces_item_data in self.workspaces:
            workspaces_item = workspaces_item_data.to_dict()
            workspaces.append(workspaces_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
                "workspaces": workspaces,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.me_user import MeUser
        from ..models.workspace import Workspace

        d = dict(src_dict)
        user = MeUser.from_dict(d.pop("user"))

        workspaces = []
        _workspaces = d.pop("workspaces")
        for workspaces_item_data in _workspaces:
            workspaces_item = Workspace.from_dict(workspaces_item_data)

            workspaces.append(workspaces_item)

        me = cls(
            user=user,
            workspaces=workspaces,
        )

        me.additional_properties = d
        return me

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
