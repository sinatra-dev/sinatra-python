from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.pull_request import PullRequest


T = TypeVar("T", bound="Task")


@_attrs_define
class Task:
    """A task: one piece of work Sinatra does, from any source.

    Attributes:
        id (str): The task's id. Use it as `taskId` in the task endpoints.
        status (str): Where the task is in its life, such as `pending`, `implementing`, `replied`, `pr_open` or
            `completed`. New statuses can appear, so don't treat the list as closed. See [Raw
            statuses](https://docs.sinatra.dev/docs/getting-started/how-it-works#raw-statuses) for each one.
        source (str): Where the task started: `api` for the CLI, MCP, this API or the dashboard, `linear` or
            `github_issue` for an issue, `slack` or `telegram` for a chat. Other sources can appear, so treat an unknown
            value as a task started elsewhere.
        title (None | str): The task's title: its issue's title, or a chat task's name. `null` for a task whose issue
            has no title, or a chat task not yet named.
        repo (None | str): `owner/name` of the task's repository. `null` until a repository is chosen.
        pull_request (None | PullRequest): The task's pull request. `null` until one opens.
        queued (bool): `true` while the task's agent waits because the workspace is already running as many agents at a
            time as its plan allows. The dashboard shows this as Waiting.
        created_at (datetime.datetime): When the task was created.
        last_activity_at (datetime.datetime | None): When the task last did something. `null` if it hasn't yet.
        url (None | str): The task's page in the Sinatra dashboard, where anyone in the workspace can follow it. On a
            task started from the CLI, MCP, API or dashboard they can reply there too.
    """

    id: str
    status: str
    source: str
    title: None | str
    repo: None | str
    pull_request: None | PullRequest
    queued: bool
    created_at: datetime.datetime
    last_activity_at: datetime.datetime | None
    url: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.pull_request import PullRequest

        id = self.id

        status = self.status

        source = self.source

        title: None | str
        title = self.title

        repo: None | str
        repo = self.repo

        pull_request: dict[str, Any] | None
        if isinstance(self.pull_request, PullRequest):
            pull_request = self.pull_request.to_dict()
        else:
            pull_request = self.pull_request

        queued = self.queued

        created_at = self.created_at.isoformat()

        last_activity_at: None | str
        if isinstance(self.last_activity_at, datetime.datetime):
            last_activity_at = self.last_activity_at.isoformat()
        else:
            last_activity_at = self.last_activity_at

        url: None | str
        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "source": source,
                "title": title,
                "repo": repo,
                "pullRequest": pull_request,
                "queued": queued,
                "createdAt": created_at,
                "lastActivityAt": last_activity_at,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.pull_request import PullRequest

        d = dict(src_dict)
        id = d.pop("id")

        status = d.pop("status")

        source = d.pop("source")

        def _parse_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        title = _parse_title(d.pop("title"))

        def _parse_repo(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        repo = _parse_repo(d.pop("repo"))

        def _parse_pull_request(data: object) -> None | PullRequest:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pull_request_type_0 = PullRequest.from_dict(data)

                return pull_request_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PullRequest, data)

        pull_request = _parse_pull_request(d.pop("pullRequest"))

        queued = d.pop("queued")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        def _parse_last_activity_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_activity_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_activity_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_activity_at = _parse_last_activity_at(d.pop("lastActivityAt"))

        def _parse_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        url = _parse_url(d.pop("url"))

        task = cls(
            id=id,
            status=status,
            source=source,
            title=title,
            repo=repo,
            pull_request=pull_request,
            queued=queued,
            created_at=created_at,
            last_activity_at=last_activity_at,
            url=url,
        )

        task.additional_properties = d
        return task

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
