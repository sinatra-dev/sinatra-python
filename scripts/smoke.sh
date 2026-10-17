#!/usr/bin/env bash
# Installs a built wheel into a clean venv (no dev dependencies, outside the
# source tree) and runs scripts/smoke.py with it.
#
#   bash scripts/smoke.sh <python-version> <wheel>
set -euo pipefail
python=$1
wheel=$(cd "$(dirname "$2")" && pwd)/$(basename "$2")
smoke=$(cd "$(dirname "$0")" && pwd)/smoke.py

venv=$(mktemp -d)
trap 'rm -rf "$venv"' EXIT
uv venv -q --python "$python" "$venv"
uv pip install -q --python "$venv/bin/python" "$wheel"
cd "$venv"
"$venv/bin/python" -c "from sinatra_dev import Sinatra"
"$venv/bin/python" "$smoke"
