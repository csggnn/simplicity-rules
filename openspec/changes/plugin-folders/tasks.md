# Tasks

## 1. Plugin folder and registry

- [x] 1.1 Move `.claude-plugin/plugin.json` to `plugins/v0/.claude-plugin/plugin.json` and set
  `"name": "v0"`. Verify `claude --plugin-dir plugins/v0` starts a session that lists the
  plugin.
- [x] 1.2 Create `plugins/v0/EVALUATION.md`: `State: default`, goal and scope (baseline
  with no skills or hooks, for any task and language), the job-search-bench comparisons that used it
  (`2026-10-15-csg-57-commute-city-level-fallback-r3` as X, and both arms of
  `...-r3-noise`), an assessment, and the decision. Verify the first line reads `State: default`.
- [x] 1.3 Create `plugins.toml` with `default = "v0"` and `[plugins.v0] state = "default"`.
  Verify it parses with `python3 -c "import tomllib; tomllib.load(open('plugins.toml','rb'))"`.
- [x] 1.4 Create `.claude-plugin/marketplace.json` named `simplicity-rules`, with entries `v0`
  (`./plugins/v0`) and `simplicity-rules` (`./plugins/v0`, `"strict": false`), each with a one-line
  `description` of the goal and scope. Verify `claude plugin validate .` passes.

## 2. Consistency check

- [x] 2.1 Write `scripts/check-plugins.py` covering every failure in the spec's check
  requirement. Verify it passes on the repository and fails, naming the plugin, when
  `plugins.toml` sets v0 to `archived`, when the marketplace omits v0, when the marketplace
  lists an archived plugin, when an offered plugin has no description, when the
  `simplicity-rules` entry points at another folder, and when `EVALUATION.md` states another
  state.
- [x] 2.2 Add the check as a local hook in `.pre-commit-config.yaml`. Verify
  `uvx pre-commit run --all-files` runs and passes it.

## 3. Marketplace behavior

- [x] 3.1 In a scratch `CLAUDE_CONFIG_DIR`, add the marketplace from the working tree and
  install `simplicity-rules@simplicity-rules` and `v0@simplicity-rules`. Verify both read
  from `plugins/v0`.
- [x] 3.2 In the same scratch config, add a second plugin folder as a temporary default,
  update the marketplace and the `simplicity-rules` plugin, and verify it reads from the new
  folder while `v0@simplicity-rules` still reads from `plugins/v0`. Discard the temporary
  plugin.

## 4. Repository files

- [x] 4.1 Verify `scripts/check-versions.sh` still reports `claude` and `uv` from the
  repository root.
- [x] 4.2 Rewrite `README.md`: plugin catalog layout, states, the procedures to add a
  candidate, make a plugin the default, make it opt-in, archive it and delete it, the
  automatic and manual ways for a project to use the default, loading for one session,
  requirements and permissions, evaluation with job-search-bench, and the
  existing Development section. Verify every section describes plugin use or development.
- [x] 4.3 Write `CLAUDE.md` with the catalog rules and the check command. Verify it names
  `plugins.toml`, `.claude-plugin/marketplace.json`, `EVALUATION.md` and
  `scripts/check-plugins.py`.

## 5. Temporary tags

- [x] 5.1 Create and push tags `plugins/v0-fcbb2ac` on `fcbb2ac` and
  `plugins/cc-review-49412cc` on `49412cc`. Verify `git ls-remote --tags origin` lists both.

## 6. Checks

- [ ] 6.1 Run `uvx pre-commit run --all-files` and `openspec validate --all`. Verify both
  pass, and CI passes on the pull request.
