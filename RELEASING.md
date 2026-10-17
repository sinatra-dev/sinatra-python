# Releasing

Releases are automatic. `.github/workflows/release.yml` runs every hour, on every push to `main`, and on demand. It has three jobs, each with only the access it needs:

1. **build** (read-only token, no stored git credentials). Fetches the live spec from `https://api.sinatra.dev/openapi.json`. If it matches the committed `openapi.json` and no release-worthy commit landed since the last `vX.Y.Z` tag, the run stops there. Release-worthy means touching `src/`, `pyproject.toml`, `openapi-python-client.yaml` or `build-constraints.txt`; docs, CI, test and lockfile-only commits wait for the next release. Otherwise it writes the live spec to `openapi.json`, regenerates `src/sinatra_dev/_generated`, runs ruff and mypy, the unit tests, the contract tests against `prism mock openapi.json` and the `next-version.sh` tests. It then computes the version with `scripts/next-version.sh` (`oasdiff` decides whether the spec change is breaking, additive or neither; with no tag yet it's `0.1.0`), sets it in `pyproject.toml` and `uv.lock`, commits the release locally, builds the sdist and wheel from that commit (`scripts/build.sh`: the build backend and its dependencies are pinned by hash in `build-constraints.txt`), and smoke-tests the wheel in clean Python 3.11 and 3.14 venvs. The sdist, the wheel, their sha256s, the release commit (as a git bundle) and the release notes are uploaded as the run's `release` artifact.
2. **publish** (PyPI OIDC token only, GitHub environment `pypi`, installs nothing). Refuses if `main` moved since the build. It hashes the artifact's `dist/` itself, which must hold exactly this version's sdist and wheel, matching the sha256s the build recorded. Then it compares them with what PyPI already has for the version (`https://pypi.org/pypi/sinatra-dev/<version>/json`): it refuses if PyPI has a file this build didn't make, skips the upload if PyPI has them all, and otherwise uploads both with `pypa/gh-action-pypi-publish`, through trusted publishing (no PyPI token is stored anywhere). There's no `skip-existing`: PyPI accepts a byte-identical file again and refuses a different one under the same name, so a stale read of PyPI's JSON can't let a different file through. After the upload it reads PyPI's JSON again, retrying for up to 5 minutes for CDN lag, and fails unless PyPI lists every built file with its sha256.
3. **tag** (write token only, installs nothing). Checks the release commit: exactly one commit on top of the commit the build started from, changing only `openapi.json`, `src/sinatra_dev/_generated/`, and the version in `pyproject.toml` and `uv.lock`. Then it pushes it (`chore(release): vX.Y.Z`) and the `vX.Y.Z` tag to `main` in one atomic push, and creates the GitHub release, whose notes are the `oasdiff` changelog.

**publish** and **tag** run only when the repository variable `PUBLISH_ENABLED` is `true`, the run is on `main`, and it isn't a dry run. Otherwise **build** ends with a notice saying what a real run would release, and the run succeeds. Runs never overlap (concurrency group `release`).

hatchling's builds are reproducible: the same tree always builds the same sdist and wheel, byte for byte. That is what lets a rerun recognise its own files on PyPI.

## When something fails

- **build fails** (the spec can't be fetched, the regenerated code doesn't typecheck, a test fails): nothing is published or tagged. Every later run fails the same way until the cause is fixed, for example by updating the wrapper for an operation the API removed.
- **publish refuses because `main` moved**: nothing is published. The push to `main` already started the run that releases the new `main`.
- **publish can't reach PyPI, or the upload fails**: nothing is tagged. The next run retries. If the upload stopped between the two files, the next run sees the one that made it, checks that it matches, and uploads both (PyPI accepts the identical one again).
- **the upload is refused with `400 File already exists`**: PyPI already has a different file under that name, which a stale read of its JSON hid from the check. Nothing is tagged, and every later run fails at the check once the JSON catches up. Recover as below.
- **PyPI doesn't list the files after the upload** (`PyPI still doesn't list all of this build's files`): nothing is tagged. If they show up later, the next run finds them, skips the upload and tags.
- **tag fails after publish**, for example when its push is rejected: PyPI now has `X.Y.Z` with no tag. On the next run, if `main` hasn't changed, it rebuilds the same files, sees the same sha256s on PyPI, skips the upload and pushes the tag. If `main` has changed, the rebuild differs, and publish fails on every run with `already on PyPI with a file this build didn't make`, rather than tagging code that was never published. Recover as below.
- **the GitHub release fails after the tag was pushed**: the next run notices the tag without a release and creates it.

### A run failed after publishing

When publish keeps failing with `sinatra-dev X.Y.Z is already on PyPI with a file this build didn't make`, an earlier run published `X.Y.Z` and never pushed its tag. Tag the commit it published from its artifact (kept for 90 days):

```sh
# The run whose tag job failed, the first one that published X.Y.Z:
gh run list --workflow release.yml --repo sinatra-dev/sinatra-python
gh run download <run-id> --name release --dir release-state --repo sinatra-dev/sinatra-python

# Check that it's the one PyPI has: the two lists must match.
sort release-state/sha256s
curl -fsS "https://pypi.org/pypi/sinatra-dev/$(cat release-state/version)/json" |
  jq -r '.urls[] | "\(.digests.sha256)  \(.filename)"' | sort

# Tag the commit that was published, and push only the tag.
git fetch release-state/release.bundle HEAD
v="v$(cat release-state/version)"
git tag -a "$v" FETCH_HEAD -m "$v"
git push origin "$v"
```

The tag points at a commit that isn't on `main`, which is fine: releases count the highest `vX.Y.Z` tag, wherever it is. The next run creates that tag's GitHub release and releases `main` as the next version.

PyPI never accepts a file name twice, even after the file is deleted, so a version can't be "fixed" in place: release the next one.

## One-time setup

PyPI can trust a workflow for a project that doesn't exist yet (a "pending publisher"), so there's no manual first upload: the workflow's first run creates `sinatra-dev` on PyPI and publishes `0.1.0`. Until that run, the name isn't reserved, so do these steps together.

1. On pypi.org, logged in as the account that should own the project: **Your account → Publishing → Add a new pending publisher → GitHub**, and enter:

   - PyPI Project Name: `sinatra-dev`
   - Owner: `sinatra-dev`
   - Repository name: `sinatra-python`
   - Workflow name: `release.yml`
   - Environment name: `pypi`

   Save. The publisher only accepts uploads from that workflow running in that environment.

2. Create the `pypi` environment in the repository, and let only `main` deploy to it:

   ```sh
   gh api -X PUT repos/sinatra-dev/sinatra-python/environments/pypi \
     -F 'deployment_branch_policy[protected_branches]=false' \
     -F 'deployment_branch_policy[custom_branch_policies]=true'
   gh api -X POST repos/sinatra-dev/sinatra-python/environments/pypi/deployment-branch-policies \
     -f name=main -f type=branch
   ```

   (or **Settings → Environments → New environment**, then **Deployment branches and tags → Selected branches → main**). Don't add required reviewers: the hourly runs would wait on them.

3. Check that GitHub Actions may push to `main`: no branch rule or ruleset may block `github-actions[bot]` from pushing commits and `v*` tags.

4. Set the repository variable that opens the gate:

   ```sh
   gh variable set PUBLISH_ENABLED --body true --repo sinatra-dev/sinatra-python
   ```

   (or **Settings → Secrets and variables → Actions → Variables → New repository variable**).

5. Start a release instead of waiting for the hourly run, watch it, then check PyPI and a clean install:

   ```sh
   gh workflow run release.yml --repo sinatra-dev/sinatra-python
   sleep 10   # the run takes a moment to appear
   gh run watch --repo sinatra-dev/sinatra-python \
     "$(gh run list --workflow release.yml --event workflow_dispatch --repo sinatra-dev/sinatra-python --limit 1 --json databaseId --jq '.[0].databaseId')"
   curl -fsS https://pypi.org/pypi/sinatra-dev/json | jq -r .info.version   # 0.1.0

   python3 -m venv /tmp/sinatra-dev-check
   /tmp/sinatra-dev-check/bin/pip install sinatra-dev==0.1.0
   /tmp/sinatra-dev-check/bin/python -c "from sinatra_dev import Sinatra"
   ```

   (`pip` needs Python 3.11 or later for this package.)

To stop releases at any time, set `PUBLISH_ENABLED` to anything but `true`.

## Dry runs

On GitHub, run the workflow with `dry_run` set: **build** runs in full, and **publish** and **tag** are skipped.

```sh
gh workflow run release.yml --repo sinatra-dev/sinatra-python -f dry_run=true
```

Locally, **build**'s steps run with `scripts/release.sh`. They rewrite `openapi.json`, `pyproject.toml` and `uv.lock` and make a local release commit, so use a scratch clone:

```sh
git clone https://github.com/sinatra-dev/sinatra-python.git /tmp/sinatra-python-dry-run && cd /tmp/sinatra-python-dry-run
uv sync --locked && bash scripts/install-oasdiff.sh
bash scripts/release.sh plan        # SPEC_FILE=path/to/spec.json to use a local spec; needs gh auth
bash scripts/generate.sh && uv run ruff check . && uv run mypy
uv run pytest && bash scripts/contract.sh
bash scripts/release.sh version     # prints the version and the release notes
bash scripts/release.sh pack        # release commit, sdist and wheel in release-state/ (via scripts/build.sh)
bash scripts/smoke.sh 3.11 release-state/dist/*.whl
DRY_RUN=true bash scripts/release.sh gate
```

`bash scripts/release.sh check` and `verify` only read (git and PyPI), so they're safe to run too. Don't run `tag` locally: it pushes to GitHub.

## Tools

The generator (`openapi-python-client`), ruff, mypy and pytest are pinned exactly in `pyproject.toml`'s `dev` group and locked in `uv.lock`; the workflows pin uv itself (`0.13.1`). The build backend (`hatchling`) and everything it installs into the isolated build are pinned by hash in `build-constraints.txt`, which `scripts/build.sh` passes to `uv build --build-constraints … --require-hashes`; regenerate it with the command at its top after changing `[build-system] requires`. Prism is locked in `scripts/prism/package-lock.json`, and `oasdiff` is pinned, with checksums, in `scripts/install-oasdiff.sh`. Bumping the generator or ruff usually changes `src/sinatra_dev/_generated`; regenerate and commit in the same change, or CI fails the drift check.

`scripts/next-version.sh` and `scripts/next-version.test.sh` are shared byte for byte with `sinatra-node` and `sinatra-go`. Change them in all three.

GitHub turns off scheduled workflows in a public repository after 60 days without activity. If releases stop, re-enable the workflow on the **Actions** tab.
