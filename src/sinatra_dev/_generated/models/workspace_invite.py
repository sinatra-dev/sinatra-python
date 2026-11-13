from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkspaceInvite")


@_attrs_define
class WorkspaceInvite:
    """An invitation's public metadata. No invitation token or redemption secret is returned.

    Attributes:
        id (str):
        email (str):
        role (str):
        status (str): active, revoked, expired, consumed or declined.
        expires_at (datetime.datetime):
        revoked_at (datetime.datetime | None):
        declined_at (datetime.datetime | None):
        accepted_at (datetime.datetime | None):
        created_at (datetime.datetime):
    """

    id: str
    email: str
    role: str
    status: str
    expires_at: datetime.datetime
    revoked_at: datetime.datetime | None
    declined_at: datetime.datetime | None
    accepted_at: datetime.datetime | None
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        email = self.email

        role = self.role

        status = self.status

        expires_at = self.expires_at.isoformat()

        revoked_at: None | str
        if isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        declined_at: None | str
        if isinstance(self.declined_at, datetime.datetime):
            declined_at = self.declined_at.isoformat()
        else:
            declined_at = self.declined_at

        accepted_at: None | str
        if isinstance(self.accepted_at, datetime.datetime):
            accepted_at = self.accepted_at.isoformat()
        else:
            accepted_at = self.accepted_at

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "email": email,
                "role": role,
                "status": status,
                "expiresAt": expires_at,
                "revokedAt": revoked_at,
                "declinedAt": declined_at,
                "acceptedAt": accepted_at,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        email = d.pop("email")

        role = d.pop("role")

        status = d.pop("status")

        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))

        def _parse_revoked_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = datetime.datetime.fromisoformat(data)

                return revoked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        revoked_at = _parse_revoked_at(d.pop("revokedAt"))

        def _parse_declined_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                declined_at_type_0 = datetime.datetime.fromisoformat(data)

                return declined_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        declined_at = _parse_declined_at(d.pop("declinedAt"))

        def _parse_accepted_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                accepted_at_type_0 = datetime.datetime.fromisoformat(data)

                return accepted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        accepted_at = _parse_accepted_at(d.pop("acceptedAt"))

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        workspace_invite = cls(
            id=id,
            email=email,
            role=role,
            status=status,
            expires_at=expires_at,
            revoked_at=revoked_at,
            declined_at=declined_at,
            accepted_at=accepted_at,
            created_at=created_at,
        )

        workspace_invite.additional_properties = d
        return workspace_invite

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
