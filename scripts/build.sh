#!/usr/bin/env bash
# Builds the sdist and wheel into <out-dir> (default dist/) with the build
# backend and every one of its dependencies pinned by hash in
# build-constraints.txt, so the isolated build environment is locked too.
#
#   bash scripts/build.sh [<out-dir>] [uv build options...]
set -euo pipefail
cd "$(dirname "$0")/.."
out=${1:-dist}
shift || true
uv build --build-constraints build-constraints.txt --require-hashes -o "$out" "$@"
