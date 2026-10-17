from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DelegateLinearTicket")


@_attrs_define
class DelegateLinearTicket:
    """A Linear issue to delegate, by its identifier or id.

    Attributes:
        source (Literal['linear']): `linear` to delegate a Linear issue.
        id (str): The issue's identifier, such as `ENG-123`, or its id.
    """

    source: Literal["linear"]
    id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        source = cast(Literal["linear"], d.pop("source"))
        if source != "linear":
            raise ValueError(f"source must match const 'linear', got '{source}'")

        id = d.pop("id")

        delegate_linear_ticket = cls(
            source=source,
            id=id,
        )

        delegate_linear_ticket.additional_properties = d
        return delegate_linear_ticket

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
