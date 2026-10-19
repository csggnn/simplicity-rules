# Proposal

## Why

The cc-review plugin exists only on the branch `candidate/cognitive-complexity`. Using it
requires a checkout or a pinned commit, and it cannot be selected through the marketplace.
It was compared with sr-v0 on one simple task. It used more effort and gave a limited
qualitative improvement. It is kept for an experiment on a more complex task, so it needs a
place in the plugin catalog.

## What Changes

- sr-cc-review is a plugin of the catalog on the default branch, in the state `candidate`.
  It holds the cc-review plugin under a name with the `sr-` prefix.
- sr-cc-review can be selected through the marketplace by name and loaded for one session
  from its folder.
- sr-cc-review behaves as cc-review did on its branch: at session start it gives the rule to
  run a design review and a cognitive complexity check on changed Python code before
  committing, and it provides the two skills that do this.
- sr-cc-review states its goal, its scope and its evaluation status, including the result of
  the comparison with sr-v0 and the open question it awaits.
- CLAUDE.md and the README's "Add a candidate" procedure state that a plugin's content names
  the plugin's own skills `<name>:<skill>`.
- sr-v0 stays the default plugin.
- The branch `candidate/cognitive-complexity` is deleted once the plugin is on the default
  branch.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `plugin-catalog`: the scenario that fixes sr-v0 as the only plugin no longer holds. The
  state requirement states the catalog's states without naming one change.

## Impact

- New plugin folder `plugins/sr-cc-review`, `plugins.toml`, `.claude-plugin/marketplace.json`.
- One line each in CLAUDE.md and README.md.
- job-search-bench can load sr-cc-review from a plugin folder instead of commit `49412cc`.
  The bench change is made in that repository.
- The branch `candidate/cognitive-complexity` is deleted on the remote and locally. The tag
  `plugins/cc-review-49412cc` keeps its commit reachable.
