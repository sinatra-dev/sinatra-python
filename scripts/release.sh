#!/usr/bin/env bash
# The release steps that .github/workflows/release.yml runs, one per command.
# Each can be run locally for a dry run (see RELEASING.md).
#
# Job "build" (read-only token, runs the dev dependencies):
#   plan     Fetch the live spec and decide whether to release: stop if it
#            matches openapi.json and no release-worthy commit landed since the
#            last tag; otherwise write it to openapi.json. Also notices a tag
#            whose GitHub release is missing (a run that failed after its push).
#   version  Compute the next version from the spec change, set it in
#            pyproject.toml (and uv.lock), write the release notes.
#   pack     Commit the release locally, save that commit as a git bundle, and
#            build the sdist and wheel from it. Everything the later jobs need
#            is then in release-state/, which the workflow uploads as an
#            artifact.
#   gate     Say whether the publish and tag jobs will run, and why not.
# Job "publish" (id-token: write, installs nothing):
#   check    Refuse if main moved since the build. Hash the artifact's dist/
#            (exactly one sdist and one wheel) and compare with what PyPI
#            already has for this version: refuse if PyPI has a file this
#            build didn't make, skip the upload if it has them all, otherwise
#            let pypa/gh-action-pypi-publish upload them (PyPI accepts a
#            byte-identical file again, so no skip-existing).
#   verify   After the upload: wait until PyPI lists every built file with
#            its sha256 (retrying for CDN lag); fail otherwise.
# Job "tag" (contents: write, installs nothing):
#   tag      Create the missing GitHub release, if any. Check the release
#            commit, push it and its vX.Y.Z tag to main in one atomic push,
#            then create the GitHub release.
#
# Environment:
#   SPEC_URL         the live spec (default https://api.sinatra.dev/openapi.json)
#   SPEC_FILE        read the spec from this file instead of SPEC_URL
#   PYPI_URL         the package index's JSON API (default https://pypi.org)
#   VERIFY_ATTEMPTS  verify's tries (default 20), VERIFY_DELAY seconds between (default 15)
#   DRY_RUN          "true" for a workflow_dispatch dry run (gate's notice only)
#   PUBLISH_ENABLED  "true" when publishing is on (gate's notice only; the
#                    workflow's job conditions are the real gate)
#   RELEASE_BRANCH   the branch releases come from and go to (default main)
set -euo pipefail
cd "$(dirname "$0")/.."

PACKAGE=sinatra-dev
GENERATED=src/sinatra_dev/_generated
SPEC_URL=${SPEC_URL:-https://api.sinatra.dev/openapi.json}
PYPI_URL=${PYPI_URL:-https://pypi.org}
BRANCH=${RELEASE_BRANCH:-main}
STATE=release-state
# Only commits touching these count as a reason to release: the package
# source (generated code included), its metadata, the generator config and
# the locked build backend.
# Docs, CI, test and lockfile-only commits wait for the next release.
RELEASE_PATHS=(src pyproject.toml openapi-python-client.yaml build-constraints.txt)
PATH="$PWD/.tools/bin:$PATH"

die() {
  if [ -n "${GITHUB_ACTIONS:-}" ]; then echo "::error title=release::$*"; else echo "release: $*" >&2; fi
  exit 1
}
notice() {
  if [ -n "${GITHUB_ACTIONS:-}" ]; then echo "::notice title=release::$*"; else echo "notice: $*"; fi
}
output() {
  if [ -n "${GITHUB_OUTPUT:-}" ]; then echo "$1" >>"$GITHUB_OUTPUT"; fi
}
summary() {
  if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then cat >>"$GITHUB_STEP_SUMMARY"; else cat; fi
}
canonical() { jq -S -c . "$1"; }
state() { cat "$STATE/$1"; }
git_bot() {
  git -c user.name="github-actions[bot]" -c user.email="41898099+github-actions[bot]@users.noreply.github.com" "$@"
}
sha256() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi
}

# Release tags, highest version first. By version, not by ancestry: a tag
# pushed by hand to recover a failed run need not be on main.
release_tags() { git tag --list 'v*' --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' || true; }

# Commits in <range> that touch the release paths, without release commits.
release_commits() {
  git log --no-merges --invert-grep --grep='^chore(release): ' --format='- %s (%h)' "$1" -- "${RELEASE_PATHS[@]}"
}

# write_notes <from-tag or ""> <to-rev> <old-spec> <new-spec> <out>
write_notes() {
  local from=$1 to=$2 old=$3 new=$4 out=$5 levels="$STATE/severity-levels.txt"
  # The spec's info.version is not the SDK's version: leave that check out.
  printf 'api-version-not-bumped none\n' >"$levels"
  local changelog=(oasdiff changelog "$old" "$new" --severity-levels "$levels")
  {
    if [ -z "$from" ]; then
      echo "First release of \`$PACKAGE\`, generated from the Sinatra API spec."
    else
      if [ "$("${changelog[@]}" --format json | jq length)" -gt 0 ]; then
        # oasdiff's markdown has its own "## API Changes" section; drop its
        # title line ("# API Changelog 1.0.0 vs. 1.0.0").
        "${changelog[@]}" --format markdown | sed '1d' | cat -s
      else
        printf '## API Changes\n\nNone.\n'
      fi
      local log
      log=$(release_commits "$from..$to")
      if [ -n "$log" ]; then
        printf '\n## Other changes\n\n%s\n' "$log"
      fi
    fi
    printf '\nAPI reference: https://docs.sinatra.dev/docs/api-reference\n'
  } >"$out"
}

step_plan() {
  rm -rf "$STATE"
  mkdir -p "$STATE"
  git rev-parse HEAD >"$STATE/base-sha"

  if [ -n "${SPEC_FILE:-}" ]; then
    cp "$SPEC_FILE" "$STATE/live.json"
  else
    curl -fsSL --retry 3 --retry-all-errors --max-time 60 -o "$STATE/live.json" "$SPEC_URL"
  fi
  jq -e '(.openapi | type == "string") and (.paths | type == "object")' "$STATE/live.json" >/dev/null ||
    die "the spec from ${SPEC_FILE:-$SPEC_URL} isn't an OpenAPI document"

  local tags tag previous
  tags=$(release_tags)
  tag=$(sed -n 1p <<<"$tags")
  previous=$(sed -n 2p <<<"$tags")
  echo "$tag" >"$STATE/last-tag"

  # A tag without a GitHub release: a run pushed its tag, then failed.
  local missing=""
  if [ -n "$tag" ]; then
    local err
    if ! err=$(gh release view "$tag" --json tagName 2>&1 >/dev/null); then
      case "$err" in
        *"release not found"*) missing=$tag ;;
        *) die "couldn't check the GitHub release for $tag: $err" ;;
      esac
    fi
  fi
  if [ -n "$missing" ]; then
    echo "$missing" >"$STATE/missing-tag"
    git show "$missing:openapi.json" >"$STATE/missing-new.json"
    if [ -n "$previous" ]; then
      git show "$previous:openapi.json" >"$STATE/missing-old.json"
    else
      cp "$STATE/missing-new.json" "$STATE/missing-old.json"
    fi
    write_notes "$previous" "$missing" "$STATE/missing-old.json" "$STATE/missing-new.json" "$STATE/missing-notes.md"
    echo "$missing has no GitHub release; the tag job will create it."
  fi
  output "missing_release=$missing"

  if [ -n "$tag" ]; then
    git show "$tag:openapi.json" >"$STATE/old.json"
  else
    cp openapi.json "$STATE/old.json"
  fi

  local spec_changed=true commits=none
  if [ "$(canonical "$STATE/live.json")" = "$(canonical openapi.json)" ]; then spec_changed=false; fi
  if [ -n "$tag" ]; then commits=$(git rev-list --count "$tag..HEAD" -- "${RELEASE_PATHS[@]}"); fi

  if [ -n "$tag" ] && [ "$spec_changed" = false ] && [ "$commits" = 0 ]; then
    echo "Nothing to release: the live spec matches openapi.json and no release-worthy commit landed since $tag."
    output "release=false"
    return 0
  fi

  # Keep the live document's key order; pretty-print so diffs stay readable.
  jq . "$STATE/live.json" >openapi.json
  echo "Releasing: last tag ${tag:-none}, spec changed: $spec_changed, release-worthy commits since the tag: $commits."
  output "release=true"
}

step_version() {
  local tag version
  tag=$(state last-tag)
  version=$(bash scripts/next-version.sh "$STATE/old.json" openapi.json "$tag")
  echo "$version" >"$STATE/version"
  # Sets [project] version and the matching line in uv.lock; nothing else.
  uv version "$version" --no-sync -q
  write_notes "$tag" HEAD "$STATE/old.json" openapi.json "$STATE/notes.md"

  output "version=$version"
  {
    echo "### v$version (last release: ${tag:-none})"
    echo
    cat "$STATE/notes.md"
  } | summary
}

step_pack() {
  local version base
  version=$(state version)
  base=$(state base-sha)

  git add -A -- openapi.json "$GENERATED" pyproject.toml uv.lock
  git_bot commit -q -m "chore(release): v$version"
  git rev-parse HEAD >"$STATE/release-sha"
  git bundle create "$STATE/release.bundle" "$base..HEAD" 2>/dev/null

  # Build from the release commit. hatchling's builds are reproducible, so a
  # rebuild of the same tree gives the same files (and sha256s).
  rm -rf "$STATE/dist"
  bash scripts/build.sh "$STATE/dist" -q --sdist --wheel
  dist_sha256s "$version" >"$STATE/sha256s"
  echo "Built from release commit $(state release-sha):"
  cat "$STATE/sha256s"
}

# dist_sha256s <version>: "sha256  filename" for each file in $STATE/dist,
# sorted, computed from the files themselves. Fails unless the directory holds
# exactly this version's sdist and wheel and nothing else.
dist_sha256s() {
  local version=$1 wheel sdist name
  wheel="sinatra_dev-$version-py3-none-any.whl"
  sdist="sinatra_dev-$version.tar.gz"
  [ -d "$STATE/dist" ] || die "$STATE/dist is missing"
  while IFS= read -r -d '' name; do
    name=${name#"$STATE/dist/"}
    [ "$name" = "$wheel" ] || [ "$name" = "$sdist" ] ||
      die "$STATE/dist holds $name; it may hold only $sdist and $wheel"
  done < <(find "$STATE/dist" -mindepth 1 -print0)
  [ -f "$STATE/dist/$wheel" ] && [ ! -L "$STATE/dist/$wheel" ] || die "$STATE/dist has no $wheel"
  [ -f "$STATE/dist/$sdist" ] && [ ! -L "$STATE/dist/$sdist" ] || die "$STATE/dist has no $sdist"
  local sha
  for name in "$sdist" "$wheel"; do
    sha=$(sha256 "$STATE/dist/$name") || die "couldn't hash $name"
    printf '%s  %s\n' "$sha" "$name"
  done | sort
}

step_gate() {
  local what
  if [ -s "$STATE/version" ]; then
    what="release v$(state version)"
  else
    what="create the missing GitHub release for $(state missing-tag)"
  fi
  if [ "${DRY_RUN:-false}" = "true" ]; then
    notice "Dry run: the publish and tag jobs are skipped. A real run would $what."
  elif [ "${PUBLISH_ENABLED:-}" != "true" ]; then
    notice "PUBLISH_ENABLED isn't 'true' (or this isn't $BRANCH): the publish and tag jobs are skipped. A real run would $what. See RELEASING.md."
  else
    echo "The publish and tag jobs run next, to $what."
  fi
}

# The commit main points at on the remote right now.
remote_head() {
  local line
  line=$(git ls-remote origin "refs/heads/$BRANCH") || die "couldn't read $BRANCH from origin"
  cut -f1 <<<"$line"
}

step_check() {
  local version base head
  version=$(state version)
  base=$(state base-sha)

  # Hash what will be uploaded, rather than trusting the artifact's list.
  local built
  built=$(dist_sha256s "$version") || exit 1
  [ "$built" = "$(sort "$STATE/sha256s")" ] ||
    die "the artifact's dist/ doesn't match the sha256s the build recorded; not publishing. Built: $(tr '\n' ' ' <"$STATE/sha256s") In dist/: $(tr '\n' ' ' <<<"$built")"
  echo "$built" >"$STATE/dist-sha256s"

  head=$(remote_head)
  if [ "$head" != "$base" ]; then
    die "$BRANCH moved from $base to $head since this run built; not publishing v$version. The next run releases the new $BRANCH."
  fi

  if ! pypi_sha256s "$version"; then
    echo "$PACKAGE $version isn't on PyPI yet; uploading it."
    output "upload=true"
    return 0
  fi

  local line missing=0
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    grep -qxF -- "$line" "$STATE/dist-sha256s" ||
      die "$PACKAGE $version is already on PyPI with a file this build didn't make ($line); this build made: $(tr '\n' ' ' <"$STATE/dist-sha256s"). A run published different code as v$version and failed before tagging it, so this run won't tag v$version on code that was never published. See RELEASING.md, 'A run failed after publishing'."
  done <"$STATE/pypi-sha256s"
  while IFS= read -r line; do
    grep -qxF -- "$line" "$STATE/pypi-sha256s" || missing=$((missing + 1))
  done <"$STATE/dist-sha256s"

  if [ "$missing" -eq 0 ]; then
    notice "$PACKAGE $version is already on PyPI with this build's files: a previous run published it and failed before tagging. Not uploading again."
    output "upload=false"
  else
    echo "$PACKAGE $version is on PyPI with $missing of this build's files missing; uploading them (the others match)."
    output "upload=true"
  fi
}

# pypi_sha256s <version>: writes what PyPI lists for the version to
# $STATE/pypi-sha256s ("sha256  filename" per file, sorted). Returns 1 when
# PyPI has no such version (404); dies on any other failure.
pypi_sha256s() {
  local url="$PYPI_URL/pypi/$PACKAGE/$1/json" code
  code=$(curl -sS --retry 3 --max-time 60 -o "$STATE/pypi.json" -w '%{http_code}' "$url") ||
    die "couldn't check whether $PACKAGE $1 is on PyPI: $url didn't answer"
  case "$code" in
    404) : >"$STATE/pypi-sha256s" && return 1 ;;
    200) ;;
    *) die "couldn't check whether $PACKAGE $1 is on PyPI: $url answered $code" ;;
  esac
  jq -r '.urls[] | "\(.digests.sha256)  \(.filename)"' "$STATE/pypi.json" | sort >"$STATE/pypi-sha256s" ||
    die "$url didn't answer with PyPI's JSON"
}

# After the upload, PyPI must list exactly this build's files. Its JSON API
# sits behind a CDN that can lag an upload, so a missing file is retried; a
# file with another sha256 (or one this build didn't make) fails at once.
step_verify() {
  local version attempts delay try line missing
  version=$(state version)
  attempts=${VERIFY_ATTEMPTS:-20}
  delay=${VERIFY_DELAY:-15}
  [ -s "$STATE/dist-sha256s" ] || die "run check first: $STATE/dist-sha256s is missing"
  for ((try = 1; try <= attempts; try++)); do
    missing=0
    if pypi_sha256s "$version"; then
      while IFS= read -r line; do
        [ -n "$line" ] || continue
        grep -qxF -- "$line" "$STATE/dist-sha256s" ||
          die "PyPI lists $line for $PACKAGE $version, which this build didn't make; this build made: $(tr '\n' ' ' <"$STATE/dist-sha256s"). Not tagging."
      done <"$STATE/pypi-sha256s"
    fi
    while IFS= read -r line; do
      grep -qxF -- "$line" "$STATE/pypi-sha256s" || missing=$((missing + 1))
    done <"$STATE/dist-sha256s"
    if [ "$missing" -eq 0 ]; then
      echo "PyPI lists every file of $PACKAGE $version with this build's sha256 (try $try)."
      return 0
    fi
    echo "PyPI doesn't list $missing of this build's files for $PACKAGE $version yet (try $try of $attempts)."
    [ "$try" -lt "$attempts" ] && sleep "$delay"
  done
  die "after $attempts tries, PyPI still doesn't list all of this build's files for $PACKAGE $version; not tagging. Built: $(tr '\n' ' ' <"$STATE/dist-sha256s")"
}

# toml_without <file> <python expression deleting the version from `d`>:
# the TOML document as canonical JSON, without its version. Needs only the
# standard library (Python 3.11+).
toml_without() {
  python3 -c '
import json, sys, tomllib
d = tomllib.loads(sys.stdin.read())
exec(sys.argv[1])
print(json.dumps(d, sort_keys=True))' "$1"
}
PYPROJECT_VERSION='del d["project"]["version"]'
LOCK_VERSION='
root = [p for p in d["package"] if p["name"] == "sinatra-dev" and p.get("source") == {"editable": "."}]
assert len(root) == 1, "uv.lock has no single editable sinatra-dev package"
del root[0]["version"]'

# Checks the release commit from the artifact before it is pushed: one commit
# on top of the commit this job checked out (the one build started from), that
# changes only the spec, the generated code and the version.
verify_release_commit() {
  local sha=$1 version=$2 base parents path
  base=$(git rev-parse HEAD)
  [ "$(state base-sha)" = "$base" ] ||
    die "the artifact was built from $(state base-sha), but this job checked out $base"
  parents=$(git rev-list --parents -n 1 "$sha" | cut -d' ' -f2-)
  [ "$parents" = "$base" ] ||
    die "release commit $sha must have exactly one parent, $base; it has: ${parents:-none}"
  # --no-renames: a rename must show its source too, or moving a file into
  # the generated directory would pass as an addition there. Written to a
  # file first, so a git failure stops the check instead of reading as "no
  # changes".
  git diff --no-renames --name-only -z "$base" "$sha" >"$STATE/release-paths" ||
    die "couldn't list the files release commit $sha changes"
  while IFS= read -r -d '' path; do
    case "$path" in
      openapi.json | pyproject.toml | uv.lock | "$GENERATED"/*) ;;
      *) die "release commit $sha changes $path; a release commit may only change openapi.json, $GENERATED/, pyproject.toml and uv.lock" ;;
    esac
  done <"$STATE/release-paths"
  # The manifests may change only their version. Each side is read on its
  # own, so a file that doesn't parse fails the check instead of comparing
  # two empty strings.
  local new_manifest old_manifest new_version
  new_manifest=$(git show "$sha:pyproject.toml" | toml_without "$PYPROJECT_VERSION") ||
    die "release commit $sha has a pyproject.toml that doesn't parse"
  old_manifest=$(git show "$base:pyproject.toml" | toml_without "$PYPROJECT_VERSION") ||
    die "$base has a pyproject.toml that doesn't parse"
  [ "$new_manifest" = "$old_manifest" ] || die "release commit $sha changes pyproject.toml beyond its version"
  new_manifest=$(git show "$sha:uv.lock" | toml_without "$LOCK_VERSION") ||
    die "release commit $sha has a uv.lock that doesn't parse"
  old_manifest=$(git show "$base:uv.lock" | toml_without "$LOCK_VERSION") ||
    die "$base has a uv.lock that doesn't parse"
  [ "$new_manifest" = "$old_manifest" ] || die "release commit $sha changes uv.lock beyond sinatra-dev's version"
  new_version=$(git show "$sha:pyproject.toml" | python3 -c 'import sys, tomllib; print(tomllib.loads(sys.stdin.read())["project"]["version"])') ||
    die "release commit $sha has no [project] version"
  [ "$new_version" = "$version" ] || die "release commit $sha sets pyproject.toml's version to $new_version, not $version"
  new_version=$(git show "$sha:uv.lock" | python3 -c '
import sys, tomllib
root = [p for p in tomllib.loads(sys.stdin.read())["package"] if p["name"] == "sinatra-dev" and p.get("source") == {"editable": "."}]
print(root[0]["version"] if len(root) == 1 else "")') || die "release commit $sha has a uv.lock that doesn't parse"
  [ "$new_version" = "$version" ] || die "release commit $sha sets uv.lock's sinatra-dev version to ${new_version:-nothing}, not $version"
}

step_tag() {
  if [ -s "$STATE/missing-tag" ]; then
    local missing
    missing=$(state missing-tag)
    gh release create "$missing" --verify-tag --title "$missing" --notes-file "$STATE/missing-notes.md"
  fi
  [ -s "$STATE/version" ] || return 0

  local version sha
  version=$(state version)
  sha=$(state release-sha)
  git fetch -q "$STATE/release.bundle" HEAD
  [ "$(git rev-parse FETCH_HEAD)" = "$sha" ] || die "release.bundle doesn't hold release commit $sha"
  verify_release_commit "$sha" "$version"
  git_bot tag -a "v$version" "$sha" -m "v$version"
  git push --atomic origin "$sha:refs/heads/$BRANCH" "refs/tags/v$version"
  gh release create "v$version" --verify-tag --title "v$version" --notes-file "$STATE/notes.md"
}

case "${1:-}" in
  plan | version | pack | gate | check | verify | tag) "step_$1" ;;
  *) die "usage: release.sh plan|version|pack|gate|check|verify|tag" ;;
esac
