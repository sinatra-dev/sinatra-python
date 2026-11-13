from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_ownership_transferred_from import (
        WorkspaceOwnershipTransferredFrom,
    )
    from ..models.workspace_ownership_transferred_to import (
        WorkspaceOwnershipTransferredTo,
    )


T = TypeVar("T", bound="WorkspaceOwnershipTransferred")


@_attrs_define
class WorkspaceOwnershipTransferred:
    """
    Attributes:
        from_ (WorkspaceOwnershipTransferredFrom):
        to (WorkspaceOwnershipTransferredTo):
    """

    from_: WorkspaceOwnershipTransferredFrom
    to: WorkspaceOwnershipTransferredTo
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_.to_dict()

        to = self.to.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_ownership_transferred_from import (
            WorkspaceOwnershipTransferredFrom,
        )
        from ..models.workspace_ownership_transferred_to import (
            WorkspaceOwnershipTransferredTo,
        )

        d = dict(src_dict)
        from_ = WorkspaceOwnershipTransferredFrom.from_dict(d.pop("from"))

        to = WorkspaceOwnershipTransferredTo.from_dict(d.pop("to"))

        workspace_ownership_transferred = cls(
            from_=from_,
            to=to,
        )

        workspace_ownership_transferred.additional_properties = d
        return workspace_ownership_transferred

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
