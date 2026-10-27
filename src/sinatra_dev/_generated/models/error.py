from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """The body of every error response.

    Attributes:
        error (str): A machine-readable code, such as `invalid_prompt`. Branch on this, not on `reason`. New codes can
            appear. Known codes: `assigned_to_other`, `bad_request`, `capacity_full`, `github_identity_required`,
            `github_not_connected`, `github_rate_limited`, `idempotency_conflict`, `internal_error`, `invalid_body`,
            `invalid_cursor`, `invalid_idempotency_key`, `invalid_limit`, `invalid_model`, `invalid_prompt`, `invalid_repo`,
            `invalid_status`, `invalid_title`, `invalid_token`, `issue_closed`, `issue_not_found`,
            `linear_app_user_missing`, `linear_identity_conflict`, `linear_identity_unlinked`, `linear_not_connected`,
            `linear_reconnect_required`, `not_an_api_task`, `not_an_issue`, `not_found`, `not_running`, `payment_required`,
            `repo_disabled`, `unavailable`.
        reason (str | Unset): A sentence saying what went wrong and, where it helps, what to do. Written to show to a
            person.
        request_id (str | Unset): The request's id. Present on some errors, not all; the `x-request-id` response header
            always carries it. Share it with support.
        refusal (str | Unset): Why a start was refused, on `payment_required` and `github_not_connected`. For
            `payment_required`: `own_credentials_required` or `subscription_inactive`. For `github_not_connected`: `missing`
            or `suspended`.
        billing_url (str | Unset): The settings section that fixes the refusal: your model credentials or billing, on
            `payment_required`; billing, when starting a task, on `capacity_full`.
        settings_url (str | Unset): The settings page that fixes the refusal, on `github_not_connected`.
        plan (str | Unset): The workspace's plan, on `capacity_full` when starting a task.
        running (int | Unset): How many agents the plan runs at a time, on `capacity_full` when starting a task.
        queued (int | Unset): How many agents the plan lets wait, on `capacity_full` when starting a task.
        task_id (str | Unset): On `unavailable` after a start: the task that was made. Retry with the same key, or send
            a message on it.
        message_id (str | Unset): On `unavailable`: the message that was saved but not sent yet. Retry with it as the
            `Idempotency-Key`.
    """

    error: str
    reason: str | Unset = UNSET
    request_id: str | Unset = UNSET
    refusal: str | Unset = UNSET
    billing_url: str | Unset = UNSET
    settings_url: str | Unset = UNSET
    plan: str | Unset = UNSET
    running: int | Unset = UNSET
    queued: int | Unset = UNSET
    task_id: str | Unset = UNSET
    message_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        reason = self.reason

        request_id = self.request_id

        refusal = self.refusal

        billing_url = self.billing_url

        settings_url = self.settings_url

        plan = self.plan

        running = self.running

        queued = self.queued

        task_id = self.task_id

        message_id = self.message_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason
        if request_id is not UNSET:
            field_dict["requestId"] = request_id
        if refusal is not UNSET:
            field_dict["refusal"] = refusal
        if billing_url is not UNSET:
            field_dict["billingUrl"] = billing_url
        if settings_url is not UNSET:
            field_dict["settingsUrl"] = settings_url
        if plan is not UNSET:
            field_dict["plan"] = plan
        if running is not UNSET:
            field_dict["running"] = running
        if queued is not UNSET:
            field_dict["queued"] = queued
        if task_id is not UNSET:
            field_dict["taskId"] = task_id
        if message_id is not UNSET:
            field_dict["messageId"] = message_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        error = d.pop("error")

        reason = d.pop("reason", UNSET)

        request_id = d.pop("requestId", UNSET)

        refusal = d.pop("refusal", UNSET)

        billing_url = d.pop("billingUrl", UNSET)

        settings_url = d.pop("settingsUrl", UNSET)

        plan = d.pop("plan", UNSET)

        running = d.pop("running", UNSET)

        queued = d.pop("queued", UNSET)

        task_id = d.pop("taskId", UNSET)

        message_id = d.pop("messageId", UNSET)

        error = cls(
            error=error,
            reason=reason,
            request_id=request_id,
            refusal=refusal,
            billing_url=billing_url,
            settings_url=settings_url,
            plan=plan,
            running=running,
            queued=queued,
            task_id=task_id,
            message_id=message_id,
        )

        error.additional_properties = d
        return error

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
