"""Lists open Linear and GitHub issues you could hand to Sinatra, yours first.
Pass one to examples/delegate_issue.py to delegate it.

    python examples/search_issues.py                   # everything open
    python examples/search_issues.py "flaky test"      # matching text
    python examples/search_issues.py "" acme/web       # search acme/web first on GitHub
"""

import sys

from sinatra_dev import Sinatra

q = sys.argv[1] if len(sys.argv) > 1 else ""
repo = sys.argv[2] if len(sys.argv) > 2 else ""

with Sinatra() as sinatra:  # reads SINATRA_TOKEN
    me = sinatra.me.get()
    if not me.workspaces:
        sys.exit("The token's user isn't in any workspace yet.")
    workspace = me.workspaces[0]

    result = sinatra.tickets.search(workspace.id, q=q or None, repo=repo or None)

if not result.linear.connected and not result.github.connected:
    print(f"{workspace.name} isn't connected to Linear or GitHub yet.")
for ticket in result.tickets:
    print(f"{'*' if ticket.yours else ' '} {ticket.identifier:<24} {ticket.title}")
n = len(result.tickets)
print(f"\n{n} issue{'' if n == 1 else 's'}. * = assigned to you or written by you.")
