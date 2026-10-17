#!/usr/bin/env bash
# Runs the contract tests: starts `prism mock openapi.json --errors` (Prism
# pinned in scripts/prism/package-lock.json) on a free port, waits for it,
# runs tests/contract against it, then stops it. Needs Node 24.18 or later.
set -euo pipefail
cd "$(dirname "$0")/.."

prism=scripts/prism/node_modules/.bin/prism
if [ ! -x "$prism" ]; then
  npm ci --prefix scripts/prism --ignore-scripts --no-audit --no-fund >/dev/null
fi

port=$(uv run --locked python -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])')
url="http://127.0.0.1:$port"

"$prism" mock openapi.json --errors -h 127.0.0.1 -p "$port" -v warn &
pid=$!
trap 'kill "$pid" 2>/dev/null || true' EXIT

for _ in $(seq 240); do
  if ! kill -0 "$pid" 2>/dev/null; then
    echo "contract: prism exited early" >&2
    exit 1
  fi
  if curl -s -o /dev/null -H 'authorization: Bearer probe' "$url/v1/me"; then
    break
  fi
  sleep 0.25
done
curl -s -o /dev/null -H 'authorization: Bearer probe' "$url/v1/me" || {
  echo "contract: prism did not start within 60s" >&2
  exit 1
}

SINATRA_CONTRACT_URL=$url uv run --locked pytest tests/contract "$@"
