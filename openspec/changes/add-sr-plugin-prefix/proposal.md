# Proposal

## Why

Claude Code namespaces a plugin's skills with the plugin's own name, the `name` in its
manifest. The name of the marketplace entry and the name of the marketplace do not appear in
the namespace. A skill of this catalog shows as `<plugin>:<skill>`, for example
`cc-review:design-review`, and the user cannot tell from it which marketplace provides the
skill. Short names such as `v0` or `cc-review` can also equal the name of a plugin from
another marketplace.

## What Changes

- Every plugin of the catalog has a name that starts with `sr-`. The skills of a plugin show
  under that name, so the namespace identifies the catalog.
- The plugin `v0` is named `sr-v0`. It keeps its content, state and evaluation status.
- The marketplace offers `sr-v0` by that name. The entry `simplicity-rules` keeps its name
  and still installs the default plugin.
- The consistency check fails when a plugin's name does not start with `sr-`.
- The documented procedures name plugins with the prefix.

## Capabilities

### New Capabilities

### Modified Capabilities
- `plugin-catalog`: plugin names carry the `sr-` prefix, and the consistency check enforces
  it.

## Impact

- `plugins/`, `plugins.toml`, `.claude-plugin/marketplace.json`, `README.md`, `CLAUDE.md`,
  the consistency check and its tests.
- A user who installed `v0@simplicity-rules` installs `sr-v0@simplicity-rules`. No project is
  known to enable `v0@simplicity-rules`.
- job-search-bench loads a plugin by folder path. A bench run on a commit after this change
  passes `plugins/sr-v0`. Saved bench results and existing git tags are unchanged.
- The cc-review candidate, added by a separate change, adopts the name `sr-cc-review`.
