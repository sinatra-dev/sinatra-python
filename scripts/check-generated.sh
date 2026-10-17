#!/usr/bin/env bash
# Fails if regenerating from the committed openapi.json changes
# src/sinatra_dev/_generated: the generated code must always be exactly what
# the pinned generator makes from the committed spec. Fix with
# `bash scripts/generate.sh` and commit the result.
set -euo pipefail
cd "$(dirname "$0")/.."

dir=src/sinatra_dev/_generated
bash scripts/generate.sh >/dev/null

if ! git diff --quiet --exit-code -- "$dir" ||
  [ -n "$(git ls-files --others --exclude-standard -- "$dir")" ]; then
  echo "$dir is out of date with openapi.json. Run 'bash scripts/generate.sh' and commit the result:" >&2
  git status --short -- "$dir" >&2
  git --no-pager diff --stat -- "$dir" >&2
  exit 1
fi
echo "$dir matches openapi.json"
