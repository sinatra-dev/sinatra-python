from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_overview_default_model_type_0 import (
        WorkspaceOverviewDefaultModelType0,
    )
    from ..models.workspace_overview_github import WorkspaceOverviewGithub
    from ..models.workspace_overview_linear import WorkspaceOverviewLinear
    from ..models.workspace_overview_plan_status_type_0 import (
        WorkspaceOverviewPlanStatusType0,
    )
    from ..models.workspace_overview_plan_status_type_1 import (
        WorkspaceOverviewPlanStatusType1,
    )
    from ..models.workspace_overview_repos_item import WorkspaceOverviewReposItem
    from ..models.workspace_overview_slack import WorkspaceOverviewSlack
    from ..models.workspace_overview_telegram import WorkspaceOverviewTelegram


T = TypeVar("T", bound="WorkspaceOverview")


@_attrs_define
class WorkspaceOverview:
    """Read-only workspace overview, with the same member-visible data as the dashboard. No credentials or tokens.

    Attributes:
        id (str): The workspace's id. Use it as `workspaceId` in the workspace endpoints.
        name (str): The workspace's name.
        role (str): Your role in it: `owner`, `admin` or `member`. New roles can appear.
        repo_environments_stage (str): Repository environments rollout stage: `off`, `prepare` or `live`.
        repo_environments_enabled (bool):
        github (WorkspaceOverviewGithub):
        linear (WorkspaceOverviewLinear):
        slack (WorkspaceOverviewSlack):
        telegram (WorkspaceOverviewTelegram):
        repos (list[WorkspaceOverviewReposItem]):
        repo_catalog (str): `none` without GitHub, `syncing` before its catalog is published, `ready` once published, or
            `suspended`. An empty repository list while syncing doesn't mean there are no connected repositories.
        plan_status (WorkspaceOverviewPlanStatusType0 | WorkspaceOverviewPlanStatusType1):
        default_model (None | WorkspaceOverviewDefaultModelType0): The workspace's saved model default, or null when
            unset. Personal and repository overrides aren't included.
    """

    id: str
    name: str
    role: str
    repo_environments_stage: str
    repo_environments_enabled: bool
    github: WorkspaceOverviewGithub
    linear: WorkspaceOverviewLinear
    slack: WorkspaceOverviewSlack
    telegram: WorkspaceOverviewTelegram
    repos: list[WorkspaceOverviewReposItem]
    repo_catalog: str
    plan_status: WorkspaceOverviewPlanStatusType0 | WorkspaceOverviewPlanStatusType1
    default_model: None | WorkspaceOverviewDefaultModelType0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.workspace_overview_default_model_type_0 import (
            WorkspaceOverviewDefaultModelType0,
        )
        from ..models.workspace_overview_plan_status_type_0 import (
            WorkspaceOverviewPlanStatusType0,
        )

        id = self.id

        name = self.name

        role = self.role

        repo_environments_stage = self.repo_environments_stage

        repo_environments_enabled = self.repo_environments_enabled

        github = self.github.to_dict()

        linear = self.linear.to_dict()

        slack = self.slack.to_dict()

        telegram = self.telegram.to_dict()

        repos = []
        for repos_item_data in self.repos:
            repos_item = repos_item_data.to_dict()
            repos.append(repos_item)

        repo_catalog = self.repo_catalog

        plan_status: dict[str, Any]
        if isinstance(self.plan_status, WorkspaceOverviewPlanStatusType0):
            plan_status = self.plan_status.to_dict()
        else:
            plan_status = self.plan_status.to_dict()

        default_model: dict[str, Any] | None
        if isinstance(self.default_model, WorkspaceOverviewDefaultModelType0):
            default_model = self.default_model.to_dict()
        else:
            default_model = self.default_model

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "role": role,
                "repoEnvironmentsStage": repo_environments_stage,
                "repoEnvironmentsEnabled": repo_environments_enabled,
                "github": github,
                "linear": linear,
                "slack": slack,
                "telegram": telegram,
                "repos": repos,
                "repoCatalog": repo_catalog,
                "planStatus": plan_status,
                "defaultModel": default_model,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.workspace_overview_default_model_type_0 import (
            WorkspaceOverviewDefaultModelType0,
        )
        from ..models.workspace_overview_github import WorkspaceOverviewGithub
        from ..models.workspace_overview_linear import WorkspaceOverviewLinear
        from ..models.workspace_overview_plan_status_type_0 import (
            WorkspaceOverviewPlanStatusType0,
        )
        from ..models.workspace_overview_plan_status_type_1 import (
            WorkspaceOverviewPlanStatusType1,
        )
        from ..models.workspace_overview_repos_item import WorkspaceOverviewReposItem
        from ..models.workspace_overview_slack import WorkspaceOverviewSlack
        from ..models.workspace_overview_telegram import WorkspaceOverviewTelegram

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        role = d.pop("role")

        repo_environments_stage = d.pop("repoEnvironmentsStage")

        repo_environments_enabled = d.pop("repoEnvironmentsEnabled")

        github = WorkspaceOverviewGithub.from_dict(d.pop("github"))

        linear = WorkspaceOverviewLinear.from_dict(d.pop("linear"))

        slack = WorkspaceOverviewSlack.from_dict(d.pop("slack"))

        telegram = WorkspaceOverviewTelegram.from_dict(d.pop("telegram"))

        repos = []
        _repos = d.pop("repos")
        for repos_item_data in _repos:
            repos_item = WorkspaceOverviewReposItem.from_dict(repos_item_data)

            repos.append(repos_item)

        repo_catalog = d.pop("repoCatalog")

        def _parse_plan_status(
            data: object,
        ) -> WorkspaceOverviewPlanStatusType0 | WorkspaceOverviewPlanStatusType1:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                plan_status_type_0 = WorkspaceOverviewPlanStatusType0.from_dict(data)

                return plan_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            plan_status_type_1 = WorkspaceOverviewPlanStatusType1.from_dict(data)

            return plan_status_type_1

        plan_status = _parse_plan_status(d.pop("planStatus"))

        def _parse_default_model(
            data: object,
        ) -> None | WorkspaceOverviewDefaultModelType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                default_model_type_0 = WorkspaceOverviewDefaultModelType0.from_dict(
                    data
                )

                return default_model_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | WorkspaceOverviewDefaultModelType0, data)

        default_model = _parse_default_model(d.pop("defaultModel"))

        workspace_overview = cls(
            id=id,
            name=name,
            role=role,
            repo_environments_stage=repo_environments_stage,
            repo_environments_enabled=repo_environments_enabled,
            github=github,
            linear=linear,
            slack=slack,
            telegram=telegram,
            repos=repos,
            repo_catalog=repo_catalog,
            plan_status=plan_status,
            default_model=default_model,
        )

        workspace_overview.additional_properties = d
        return workspace_overview

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
