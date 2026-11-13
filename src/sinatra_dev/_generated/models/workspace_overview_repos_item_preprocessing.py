from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_overview_repos_item_preprocessing_label import (
        WorkspaceOverviewReposItemPreprocessingLabel,
    )
    from ..models.workspace_overview_repos_item_preprocessing_metadata import (
        WorkspaceOverviewReposItemPreprocessingMetadata,
    )


T = TypeVar("T", bound="WorkspaceOverviewReposItemPreprocessing")


@_attrs_define
class WorkspaceOverviewReposItemPreprocessing:
    """
    Attributes:
        overall_status (str):
        metadata (WorkspaceOverviewReposItemPreprocessingMetadata):
        label (WorkspaceOverviewReposItemPreprocessingLabel):
    """

    overall_status: str
    metadata: WorkspaceOverviewReposItemPreprocessingMetadata
    label: WorkspaceOverviewReposItemPreprocessingLabel
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        overall_status = self.overall_status

        metadata = self.metadata.to_dict()

        label = self.label.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "overallStatus": overall_status,
                "metadata": metadata,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_overview_repos_item_preprocessing_label import (
            WorkspaceOverviewReposItemPreprocessingLabel,
        )
        from ..models.workspace_overview_repos_item_preprocessing_metadata import (
            WorkspaceOverviewReposItemPreprocessingMetadata,
        )

        d = dict(src_dict)
        overall_status = d.pop("overallStatus")

        metadata = WorkspaceOverviewReposItemPreprocessingMetadata.from_dict(
            d.pop("metadata")
        )

        label = WorkspaceOverviewReposItemPreprocessingLabel.from_dict(d.pop("label"))

        workspace_overview_repos_item_preprocessing = cls(
            overall_status=overall_status,
            metadata=metadata,
            label=label,
        )

        workspace_overview_repos_item_preprocessing.additional_properties = d
        return workspace_overview_repos_item_preprocessing

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
