from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkspaceOverviewGithub")


@_attrs_define
class WorkspaceOverviewGithub:
    """
    Attributes:
        status (str): `connected` or `not_connected`.
        account_login (None | str):
        account_type (None | str):
        installation_id (None | str): GitHub installation id as a decimal string.
    """

    status: str
    account_login: None | str
    account_type: None | str
    installation_id: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        account_login: None | str
        account_login = self.account_login

        account_type: None | str
        account_type = self.account_type

        installation_id: None | str
        installation_id = self.installation_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "accountLogin": account_login,
                "accountType": account_type,
                "installationId": installation_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = d.pop("status")

        def _parse_account_login(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        account_login = _parse_account_login(d.pop("accountLogin"))

        def _parse_account_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        account_type = _parse_account_type(d.pop("accountType"))

        def _parse_installation_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        installation_id = _parse_installation_id(d.pop("installationId"))

        workspace_overview_github = cls(
            status=status,
            account_login=account_login,
            account_type=account_type,
            installation_id=installation_id,
        )

        workspace_overview_github.additional_properties = d
        return workspace_overview_github

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
