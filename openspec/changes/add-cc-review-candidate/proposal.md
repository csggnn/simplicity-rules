# Proposal

## Why

The cc-review plugin exists only on the branch `candidate/cognitive-complexity`. Using it
requires a checkout or a pinned commit, and it cannot be selected through the marketplace.
It was compared with v0 on one simple task. It used more effort and gave a limited
qualitative improvement. It is kept for an experiment on a more complex task, so it needs a
place in the plugin catalog.

## What Changes

- cc-review is a plugin of the catalog on the default branch, in the state `candidate`.
- cc-review can be selected through the marketplace by name and loaded for one session from
  its folder.
- cc-review behaves as it did on its branch: at session start it gives the rule to run a
  design review and a cognitive complexity check on changed Python code before committing,
  and it provides the two skills that do this.
- cc-review states its goal, its scope and its evaluation status, including the result of
  the comparison with v0 and the open question it awaits.
- v0 stays the default plugin.
- The branch `candidate/cognitive-complexity` is deleted once the plugin is on the default
  branch.

## Capabilities

### New Capabilities
- `cc-review-plugin`: what the cc-review plugin does in a session: the rule it adds at
  session start, the design review skill and the cognitive complexity skill.

### Modified Capabilities
- `plugin-catalog`: the scenario that fixes v0 as the only plugin no longer holds. The state
  requirement states the catalog's states without naming one change.

## Impact

- New plugin folder, `plugins.toml`, `.claude-plugin/marketplace.json`.
- job-search-bench can load cc-review from a plugin folder instead of commit `49412cc`. The
  bench change is made in that repository.
- The branch `candidate/cognitive-complexity` is deleted on the remote and locally. The tag
  `plugins/cc-review-49412cc` keeps its commit reachable.
