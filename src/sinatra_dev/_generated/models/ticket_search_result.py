from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ticket import Ticket
    from ..models.ticket_search_result_github import TicketSearchResultGithub
    from ..models.ticket_search_result_linear import TicketSearchResultLinear


T = TypeVar("T", bound="TicketSearchResult")


@_attrs_define
class TicketSearchResult:
    """The issues you could delegate, and how the workspace is connected to each tracker.

    Attributes:
        tickets (list[Ticket]): The issues you could delegate. Linear issues come first, then GitHub's, each with yours
            before your team's unassigned ones.
        linear (TicketSearchResultLinear): The workspace's Linear connection, as it applies to you.
        github (TicketSearchResultGithub): The workspace's GitHub connection.
    """

    tickets: list[Ticket]
    linear: TicketSearchResultLinear
    github: TicketSearchResultGithub
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tickets = []
        for tickets_item_data in self.tickets:
            tickets_item = tickets_item_data.to_dict()
            tickets.append(tickets_item)

        linear = self.linear.to_dict()

        github = self.github.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tickets": tickets,
                "linear": linear,
                "github": github,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ticket import Ticket
        from ..models.ticket_search_result_github import TicketSearchResultGithub
        from ..models.ticket_search_result_linear import TicketSearchResultLinear

        d = dict(src_dict)
        tickets = []
        _tickets = d.pop("tickets")
        for tickets_item_data in _tickets:
            tickets_item = Ticket.from_dict(tickets_item_data)

            tickets.append(tickets_item)

        linear = TicketSearchResultLinear.from_dict(d.pop("linear"))

        github = TicketSearchResultGithub.from_dict(d.pop("github"))

        ticket_search_result = cls(
            tickets=tickets,
            linear=linear,
            github=github,
        )

        ticket_search_result.additional_properties = d
        return ticket_search_result

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
