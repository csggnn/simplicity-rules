# Design

## Context

See proposal.md for motivation and specs/plugin-catalog/spec.md for the required behavior.

### Claude Code plugin naming

- The plugins reference, section "Metadata precedence": when a marketplace entry lists a
  plugin under a different name than the manifest, `enabledPlugins` uses the entry name, and
  components are namespaced under the manifest name.
- A skill of a plugin is invoked as `<manifest name>:<skill>`.

### Repository state

- `plugins/v0/` holds the only plugin. Its manifest name is `v0`. Its state is `default`.
- `.claude-plugin/marketplace.json` lists the entries `simplicity-rules` (`"strict": false`,
  source `./plugins/v0`) and `v0`.
- `scripts/check-plugins.py` requires the manifest name to equal the folder name, and every
  marketplace entry other than `simplicity-rules` to name a plugin folder.
- `versions.toml` and `scripts/check-versions.sh` name tools, not plugins.
- The git tag `plugins/v0-fcbb2ac` keeps a commit reachable that saved job-search-bench
  results reference.

## Goals / Non-Goals

**Goals:**
- A project that enables `simplicity-rules@simplicity-rules` keeps working after this change.
- A plugin keeps one name across its folder, manifest, marketplace entry and `plugins.toml`
  table, so the existing rules and procedures apply with the prefixed name.
- The check runs offline with the Python standard library.

**Non-Goals:**
- Renaming the marketplace or its `simplicity-rules` entry.
- Renaming or deleting git tags.
- Editing saved job-search-bench results.

## Decisions

### The prefix is part of the plugin name

A plugin named `<name>` has the folder `plugins/sr-<name>/`, the manifest name `sr-<name>`,
the marketplace entry `sr-<name>` and the table `[plugins.sr-<name>]`. The rule "the manifest
name equals the folder name" stays.

Alternative: prefix the manifest name only and keep the folder name. Rejected because the
folder, the entry and the manifest would carry two names, and the check and the procedures
would map one to the other.

Alternative: prefix the marketplace entry name only. Rejected because Claude Code namespaces
components under the manifest name, so the skill names would not change.

### The prefix is `sr-`

`sr` abbreviates `simplicity-rules`. A short prefix keeps skill names short.

### The check tests the prefix of every plugin name

`scripts/check-plugins.py` reports every name in `plugins.toml` and every folder in
`plugins/` that does not start with `sr-`. The manifest name equals the folder name, and
every marketplace entry other than `simplicity-rules` names a plugin, so the check covers the
manifest and the marketplace through the existing rules. `tests/test_check_plugins.py` adds a
case with an archived plugin `old`.

### v0 is named sr-v0

`plugins/v0/` moves to `plugins/sr-v0/`. The manifest name, the marketplace entry, the
`plugins.toml` table and `default` use `sr-v0`. The `simplicity-rules` entry points at
`./plugins/sr-v0` and its description names `sr-v0`. `EVALUATION.md` names the plugin
`sr-v0`. Its setup labels (`v0`, `v0-a`, `v0-b`) are identifiers in saved job-search-bench
results and stay as they are.

The plugin keeps its state, so the first line and the Decision section of `EVALUATION.md`
do not change.

## Risks / Trade-offs

- [A user installed `v0@simplicity-rules`] → After a marketplace update the entry is gone.
  The user installs `sr-v0@simplicity-rules`. No project is known to enable it.
- [A job-search-bench run passes `plugins/v0` for a commit after this change] → The folder
  is missing and the run fails at load. The bench passes `plugins/sr-v0` for such commits.
- [A branch adding a plugin without the prefix merges after this change] → The check fails
  on that branch until it renames the plugin.
