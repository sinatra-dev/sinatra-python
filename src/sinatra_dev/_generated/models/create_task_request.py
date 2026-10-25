from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateTaskRequest")


@_attrs_define
class CreateTaskRequest:
    """A task to start.

    Attributes:
        prompt (str): What to do, as you'd ask a teammate. Up to 100,000 characters, after trimming.
        title (None | str | Unset): The task's title, up to 200 characters. Defaults to the prompt's first line, cut to
            80 characters.
        repo (None | str | Unset): `owner/name` of a repository connected to the workspace. Omit it to let the agent
            choose.
        model (None | str | Unset): A model from Sinatra's catalog, such as `anthropic/claude-opus-5-5` or `openai-
            codex/gpt-6.1-sol`, that every turn of the task runs on. The model picks its engine. Omit it to use the
            repository's or workspace's model.
    """

    prompt: str
    title: None | str | Unset = UNSET
    repo: None | str | Unset = UNSET
    model: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        repo: None | str | Unset
        if isinstance(self.repo, Unset):
            repo = UNSET
        else:
            repo = self.repo

        model: None | str | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if repo is not UNSET:
            field_dict["repo"] = repo
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        prompt = d.pop("prompt")

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_repo(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        repo = _parse_repo(d.pop("repo", UNSET))

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        create_task_request = cls(
            prompt=prompt,
            title=title,
            repo=repo,
            model=model,
        )

        create_task_request.additional_properties = d
        return create_task_request

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
