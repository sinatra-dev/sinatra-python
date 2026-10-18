"""Hands Sinatra an issue you already have, the way assigning it in Linear or
labelling it on GitHub would. Sinatra works on it in its own sandbox and opens
a draft pull request.

    python examples/delegate_issue.py ENG-123        # a Linear issue
    python examples/delegate_issue.py acme/web#42    # a GitHub issue
"""

import re
import sys

from sinatra_dev import Sinatra

if len(sys.argv) != 2:
    sys.exit("usage: python examples/delegate_issue.py <ENG-123 | owner/name#42>")
ref = sys.argv[1]

with Sinatra() as sinatra:  # reads SINATRA_TOKEN
    me = sinatra.me.get()
    if not me.workspaces:
        sys.exit("The token's user isn't in any workspace yet.")
    workspace = me.workspaces[0]

    github = re.fullmatch(r"([^/\s]+/[^#\s]+)#(\d+)", ref)
    if github:
        sinatra.tickets.delegate(workspace.id, source="github", repo=github[1], number=int(github[2]))
    else:
        sinatra.tickets.delegate(workspace.id, source="linear", id=ref)

print(f"Delegated {ref} in {workspace.name}. Sinatra will open a draft pull request.")
print("Follow it in the dashboard, or list open PRs with examples/open_prs.py.")
