"""Prints every pull request Sinatra has open and waiting for review, in each
of your workspaces, as a Markdown list you can paste into a standup or a Slack
channel.

    python examples/open_prs.py
"""

from sinatra_dev import Sinatra

with Sinatra() as sinatra:  # reads SINATRA_TOKEN
    for workspace in sinatra.me.get().workspaces:
        lines = [
            f"- [{task.title or task.pull_request.url}]({task.pull_request.url}) in {task.repo or '?'}"
            for task in sinatra.tasks.list_all(workspace.id, status="pr_open")
            if task.pull_request
        ]
        print(f"## {workspace.name}: {len(lines)} open pull request{'' if len(lines) == 1 else 's'}")
        if lines:
            print("\n".join(lines))
        print()
