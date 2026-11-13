from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_overview_repos_item_preprocessing import (
        WorkspaceOverviewReposItemPreprocessing,
    )


T = TypeVar("T", bound="WorkspaceOverviewReposItem")


@_attrs_define
class WorkspaceOverviewReposItem:
    """
    Attributes:
        id (str):
        name (str): Connected repository in `owner/name` form.
        short_description (str):
        primary_language (None | str):
        stack (None | str):
        preprocessing (WorkspaceOverviewReposItemPreprocessing):
    """

    id: str
    name: str
    short_description: str
    primary_language: None | str
    stack: None | str
    preprocessing: WorkspaceOverviewReposItemPreprocessing
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        short_description = self.short_description

        primary_language: None | str
        primary_language = self.primary_language

        stack: None | str
        stack = self.stack

        preprocessing = self.preprocessing.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "shortDescription": short_description,
                "primaryLanguage": primary_language,
                "stack": stack,
                "preprocessing": preprocessing,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_overview_repos_item_preprocessing import (
            WorkspaceOverviewReposItemPreprocessing,
        )

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        short_description = d.pop("shortDescription")

        def _parse_primary_language(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        primary_language = _parse_primary_language(d.pop("primaryLanguage"))

        def _parse_stack(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        stack = _parse_stack(d.pop("stack"))

        preprocessing = WorkspaceOverviewReposItemPreprocessing.from_dict(
            d.pop("preprocessing")
        )

        workspace_overview_repos_item = cls(
            id=id,
            name=name,
            short_description=short_description,
            primary_language=primary_language,
            stack=stack,
            preprocessing=preprocessing,
        )

        workspace_overview_repos_item.additional_properties = d
        return workspace_overview_repos_item

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
