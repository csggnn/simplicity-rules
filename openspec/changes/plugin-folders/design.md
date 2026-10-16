# Design

## Context

See proposal.md for motivation and specs/plugin-catalog/spec.md for the required behavior.

### Repository state

- `main` packages the repository root as one plugin named `simplicity-rules`. The plugin
  manifest is `.claude-plugin/plugin.json`. The marketplace `.claude-plugin/marketplace.json`
  is also named `simplicity-rules` and lists that plugin with the relative source `./`. The
  plugin holds no skills, hooks or agents.
- `scripts/check-versions.sh` and `versions.toml` (minimums for `claude` and `uv`) are at the
  repository root. `README.md` describes plugin use, evaluation and development. Pre-commit,
  CI, Dependabot, CodeRabbit and OpenSpec are set up.
- The branch `candidate/cognitive-complexity` holds a plugin at its root: `rules.md`,
  `hooks/` and two skills. A later change moves it to a plugin folder of this layout.

### Claude Code plugin loading

- `claude --plugin-dir <dir>` loads the plugin whose `.claude-plugin/plugin.json` is in
  `<dir>`. The option repeats.
- A marketplace (`.claude-plugin/marketplace.json`) lists plugins by name, each with a
  `source`. A relative `source` names a folder in the marketplace repository.
- Verified with Claude Code 2.1.300 in a scratch config dir: two marketplace entries with
  different names and the same `source`, the second with `"strict": false`, install as two
  plugins read from the same folder.
- A project enables an installed plugin with `enabledPlugins` in `.claude/settings.json` or
  `.claude/settings.local.json`.

### Consumers

- job-search-bench clones this repository at a commit and passes `--plugin-dir <clone>`. Its
  saved results reference commit `fcbb2ac`, the plugin as it was at the root, and commit
  `49412cc`, the head of `candidate/cognitive-complexity`. The results are rewritten to
  reference plugin folders. A result lost before the rewrite can be regenerated.
- job-search-agent enables no plugin.

## Goals / Non-Goals

**Goals:**
- A project that enables `simplicity-rules@simplicity-rules` keeps working after this change.
- A bench run that names a plugin folder at a commit loads the same plugin content on every
  run.
- Adding, promoting or archiving a plugin changes no other plugin's manifest or content. The
  `EVALUATION.md` of a replaced default changes, because it records the state.
- The consistency check runs offline, with no dependency beyond Python 3.11 or newer and what
  CI and pre-commit already install.

**Non-Goals:**
- Version numbers per plugin. A plugin is identified by its folder and the repository commit.
- Switching a project to a new default without a marketplace and plugin update.
- A machine-readable format for the evaluation results. The status is read by people; the
  check reads only the state.

## Decisions

### Layout

```
.claude-plugin/marketplace.json   offered plugins and the simplicity-rules entry
plugins.toml                      state of every plugin
plugins/<name>/
  .claude-plugin/plugin.json      manifest, "name" equals <name>
  EVALUATION.md                   evaluation status
  skills/, hooks/, agents/, ...   plugin content
scripts/check-versions.sh         shared: installed tools against versions.toml
scripts/check-plugins.py          consistency check
versions.toml                     shared tool minimums
README.md, CLAUDE.md
```

`versions.toml` and `check-versions.sh` stay at the repository root. Every plugin shares
the same tool minimums today.

Alternative: a separate marketplace per plugin. Rejected because the user would add one
marketplace per plugin and the default entry would have no single home.

### Plugin states in `plugins.toml`

```toml
default = "v0"

[plugins.v0]
state = "default"
```

`default` names the plugin whose state is `default`. The check requires them to agree. The
duplication makes the default readable at the top of the file.

Alternative: a custom field in each `plugin.json`. Rejected because the manifest is read by
Claude Code, and a state change would edit the plugin's own folder.

Alternative: the marketplace as the registry. Rejected because it cannot tell a `candidate`
from an `opt-in` plugin, and archived plugins are not listed there.

### The `simplicity-rules` marketplace entry follows the default

The marketplace keeps its name, `simplicity-rules`. It lists every `default`, `opt-in`
and `candidate` plugin under its folder name, and one more entry named `simplicity-rules` with
`"strict": false` whose `source` is the default plugin's folder. A project that enables
`simplicity-rules@simplicity-rules` follows the default. `main` already uses this marketplace
and plugin name, so an existing installation keeps working.

Alternative: no alias. Rejected because every project would edit its settings on each change
of default.

### Archived plugins stay in `plugins/`

Archiving sets the state to `archived` and removes the plugin's marketplace entry. The
folder stays at `plugins/<name>/`, so the path of every plugin is stable across states.
Deleting removes the folder and the state. Git history and the bench's commit references
keep it recoverable.

Alternative: move archived plugins to `archive/<name>/`. Rejected because the state already
records the archive, and the move changes the plugin's path.

### Evaluation status in `EVALUATION.md`

Each plugin folder holds `EVALUATION.md`. Its first line is `State: <state>`. Sections:
Goal and scope (the goal, the tasks the plugin is meant for and not meant for),
Comparisons (job-search-bench comparison id, setup labels, result summary),
Assessment (cost and benefit observed, open questions, next experiment), Decision (decision
and date). The check compares the first line with `plugins.toml`.

The marketplace entry `description` is a one-line summary of the Goal and scope section, so
the user sees it when choosing a plugin. It is the only copy of the summary in the catalog
files the check reads. The README does not repeat it. A plugin's manifest `description` is the
plugin's own metadata. The check requires the marketplace `description` to be non-empty and
does not compare it with `EVALUATION.md` or the manifest.

The Assessment of cc-review, added by a later change, reads: the plugin increases effort,
showed limited qualitative improvement on a simple task, and awaits an experiment on a more
complex task.

Alternative: goal and scope as fields in `plugins.toml`. Rejected because no consumer reads
them as data. A reader sees them in the marketplace listing and in `EVALUATION.md`.

### Consistency check as a pre-commit hook

`scripts/check-plugins.py` uses the Python standard library (`tomllib`, `json`, `pathlib`). It
needs Python 3.11 or newer for `tomllib`, and stops with a message on an older interpreter. A
file it cannot parse is reported as a violation.
It runs as a local pre-commit hook, so the existing CI step `pre-commit run --all-files` runs
it with no new CI step. It prints one line per violation and exits 1 on any. Ruff lints it.

Alternative: a shell script. Rejected because shell has no TOML or JSON parser, and the
check would need `jq` and a TOML tool.

### v0 is the current root plugin

`plugins/v0/.claude-plugin/plugin.json` is the root manifest moved into the folder, with
`"name": "v0"`. The root manifest is removed. The root `README.md` keeps its requirements,
install, session loading and permissions sections, updated for the catalog, and documents
the catalog.

### Minimum Claude Code version

Two marketplace entries with one source were verified with Claude Code 2.1.300. The `claude`
minimum in `versions.toml` is 2.1.300.

### Using the default in a project

The README documents two ways for a project, such as job-search-agent:

- Automatic: the project's `.claude/settings.json` declares the marketplace and enables
  `simplicity-rules@simplicity-rules`.
- Manual: each user installs the plugin and enables it in `.claude/settings.local.json`, or
  enables a named plugin to pin it.

### Temporary tags for bench commits

Tags keep the two commits that saved bench results reference reachable after
`candidate/cognitive-complexity` is deleted: `plugins/v0-fcbb2ac` on `fcbb2ac` and
`plugins/cc-review-49412cc` on `49412cc`. They are deleted once the saved results reference
plugin folders. The branch is deleted after the cc-review change is merged.

### Repository CLAUDE.md

`CLAUDE.md` states the catalog rules for sessions working on this repository: plugin folder
contents, state changes through `plugins.toml`, the marketplace and `EVALUATION.md` together,
and the check command.

## Risks / Trade-offs

- [A project enables both `simplicity-rules@simplicity-rules` and the default plugin by name,
  and loads it twice] → The README states to enable one of them.
- [A later Claude Code version rejects two entries with the same source] → The README
  procedures end with `claude plugin validate .`. The check requires `"strict": false` on the
  `simplicity-rules` entry. The fallback is the manual procedure.
- [job-search-bench passes `--plugin-dir <clone>` for a commit after this change, and the
  clone root holds no plugin manifest] → The bench passes `<clone>/plugins/<name>`. That
  change is made in job-search-bench. Earlier commits keep the root layout.
- [The default changes and a project that follows it does not update] → The project keeps the
  previous default until `claude plugin marketplace update` and `claude plugin update`.
