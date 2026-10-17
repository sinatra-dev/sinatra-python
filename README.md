# sinatra-dev

A Python client for the [Sinatra API](https://docs.sinatra.dev/docs/api-reference): start, follow and stop Sinatra tasks, and delegate Linear and GitHub issues.

It runs on Python 3.11 and later, is typed (`py.typed`), and depends only on `httpx` and `attrs`. The client is generated from the API's [OpenAPI spec](https://api.sinatra.dev/openapi.json) and released automatically when the spec changes.

## Install

```sh
pip install sinatra-dev
```

## Quick start

```python
import time

from sinatra_dev import Sinatra

# The turn is done when the task leaves these statuses (for example, it reaches replied or pr_open).
WORKING = {"pending", "investigating", "implementing", "rework"}

with Sinatra() as sinatra:  # reads SINATRA_TOKEN
    me = sinatra.me.get()
    if not me.workspaces:
        raise SystemExit("The token's user isn't in any workspace yet.")
    workspace = me.workspaces[0]

    task = sinatra.tasks.create(
        workspace.id, "Fix the flaky login test", repo="acme/web", idempotency_key="fix-flaky-login-1"
    ).task

    after = None
    while True:
        status = sinatra.tasks.get(workspace.id, task.id).status
        for m in sinatra.messages.list_all(workspace.id, task.id, after=after):
            print(f"{m.role}: {m.body}")
            after = m.id
        if status not in WORKING:
            break
        time.sleep(3)
    print(f"Task {task.id} is {status}.")
```

The API has no streaming. To wait for a reply, read the conversation after the last entry you've seen, and check the task's `status`: the agent posts one reply per turn, and the turn is done when the task stops working. The loop reads the status before the conversation, so it never stops before printing the reply that ended the turn. An unknown status counts as done, so the loop can't wait forever on a status added after this was written. See [How replies work](https://docs.sinatra.dev/docs/cli-and-api#how-replies-work).

## Authentication

Create a personal access token on the [Access tokens](https://app.sinatra.dev/tokens) page (**CLI & API** in the dashboard). It starts with `sntr_` and acts as you in every workspace you belong to. The client reads it from the `SINATRA_TOKEN` environment variable, or you can pass it:

```python
sinatra = Sinatra(token=os.environ["MY_TOKEN"])
```

The constructor raises `ValueError` if it finds no token. Other options:

- `base_url`: defaults to `https://api.sinatra.dev`.
- `timeout`: seconds each attempt may wait to connect, and for each chunk of the response, before httpx raises `httpx.TimeoutException`. Defaults to 60; `None` turns it off. An `httpx.Timeout` works too.
- `http_client`: an `httpx.Client` to send requests with, for example one with a proxy. The client doesn't close it.

Every method takes a `timeout` keyword that overrides the client's for that call:

```python
sinatra.tasks.get(workspace_id, task_id, timeout=5)
```

Use the client as a context manager, or call `sinatra.close()`, to release its connections.

## Operations

The namespaces mirror the API's operation ids:

| Method | Request |
| --- | --- |
| `me.get()` | `GET /v1/me` |
| `me.revoke_token()` | `DELETE /v1/me/token` |
| `tasks.list(workspace_id, status=, limit=, cursor=)` | `GET /v1/workspaces/{workspaceId}/tasks` |
| `tasks.get(workspace_id, task_id)` | `GET /v1/workspaces/{workspaceId}/tasks/{taskId}` |
| `tasks.create(workspace_id, prompt, title=, repo=, idempotency_key=)` | `POST /v1/workspaces/{workspaceId}/tasks` |
| `tasks.stop(workspace_id, task_id)` | `POST /v1/workspaces/{workspaceId}/tasks/{taskId}/stop` |
| `messages.create(workspace_id, task_id, text, idempotency_key=)` | `POST /v1/workspaces/{workspaceId}/tasks/{taskId}/messages` |
| `messages.list(workspace_id, task_id, after=, limit=)` | `GET /v1/workspaces/{workspaceId}/tasks/{taskId}/messages` |
| `tickets.search(workspace_id, q=, repo=)` | `GET /v1/workspaces/{workspaceId}/tickets` |
| `tickets.delegate(workspace_id, source="linear", id=)` or `(workspace_id, source="github", repo=, number=)` | `POST /v1/workspaces/{workspaceId}/tickets/delegate` |

Responses are typed objects with snake_case attributes (`task.pull_request`, `page.next_cursor`). Fields the API added after this release are kept in each object's `additional_properties`.

`tasks.list_all` and `messages.list_all` page through everything for you:

```python
for task in sinatra.tasks.list_all(workspace_id, status="pr_open"):
    print(task.id, task.title)
```

Fields such as `status`, `source`, `role`, `kind` and the error `code` are plain strings, and the API adds new values over time. Handle values you don't recognise.

## Retries and idempotency

`tasks.create` and `messages.create` always send an `Idempotency-Key`. If you don't pass one, the client makes a random UUID. Every retry of a call sends the same key, so a retried start never starts a second task. Pass your own key to make a retry safe across process restarts too.

The client retries a request up to 3 times when it's safe to repeat:

- `429`: after the `Retry-After` the server sends, at most 60 seconds.
- `503`: after 0.5s, then 1s, then 2s.

GETs, `me.revoke_token`, `tasks.create` and `messages.create` retry on both. `tasks.stop` retries on `503` only. `tickets.delegate` takes no idempotency key and is never retried. Other errors, timeouts and network failures are never retried.

## Errors

An error response raises a `SinatraError`:

```python
from sinatra_dev import SinatraError

try:
    sinatra.tasks.stop(workspace_id, task_id)
except SinatraError as err:
    if err.code != "not_running":  # not_running: the task had already stopped
        raise
```

| Attribute | |
| --- | --- |
| `status` | The HTTP status. |
| `code` | The API's `error` code, such as `capacity_full`. `http_error` when the response carried none, such as an HTML error page from a proxy. |
| `reason` | A sentence for a person. Don't branch on it. |
| `request_id` | The request's id. Include it when you contact support. |
| `body` | The response body: the parsed JSON, or the text. Refusals carry extra fields here, such as `billingUrl`. |
| `headers` | The response headers. |

Network failures and timeouts are not wrapped: they raise the `httpx.HTTPError` (for example `httpx.TimeoutException`) that httpx raised.

The [API reference](https://docs.sinatra.dev/docs/api-reference) lists every operation's error codes.

## Versions

Releases follow semver. While the version is `0.x`, a breaking API change bumps the minor version and anything else bumps the patch. From `1.0`, breaking changes bump the major version and additions bump the minor.

## Development

Needs [uv](https://docs.astral.sh/uv/), and Node 24 for the contract tests.

```sh
uv sync
bash scripts/install-oasdiff.sh   # installs the pinned oasdiff into .tools/bin
bash scripts/generate.sh          # regenerates src/sinatra_dev/_generated from openapi.json
uv run ruff check . && uv run ruff format --check . && uv run mypy
uv run pytest                     # wrapper tests against a local stub server
bash scripts/contract.sh          # every operation against a Prism mock of openapi.json
PATH="$PWD/.tools/bin:$PATH" bash scripts/next-version.test.sh
```

`src/sinatra_dev/_generated` is written by `openapi-python-client` and never edited by hand; CI fails if it differs from what `openapi.json` generates (`bash scripts/check-generated.sh`). `openapi.json` is updated by the release workflow. See [RELEASING.md](RELEASING.md).

## License

MIT
