# Proposal

## Why

The repository holds one plugin at its root. A second variant, cc-review, lives on the branch
`candidate/cognitive-complexity`. A variant kept as an option, such as cc-review for complex
features, has no place in the champion/candidate branch model. On a branch it drifts from `main`, and using it
requires a checkout or a pinned commit. No file records which plugin is the default or what
the evaluations of a plugin found. This is issue #4.

## What Changes

- Several plugins coexist on `main`. Each one can be enabled per project or loaded for one
  session, alone or together with others, without a branch checkout.
- Installing the repository's marketplace lists the plugins that can be selected: the
  default, opt-in plugins and candidates under evaluation. Deprecated plugins are not listed.
- One plugin is the default. A project can enable the default in a way that follows a change
  of default with no edit to the project, or enable a named plugin.
- Changing the default, deprecating a plugin (archived or deleted) and adding a candidate
  are documented procedures.
- Each plugin states its goal and scope: what it is meant to achieve and the tasks it is
  meant for, such as trivial tasks only, complex tasks, or one language. A user choosing a
  plugin sees the goal and scope at the point of choice.
- Each plugin states its evaluation status: its state, the bench comparisons
  that evaluated it, an assessment of its cost and benefit with the open questions, and the
  decision taken.
- A check fails when the recorded default, the plugin states, the marketplace listing and the
  plugin folders disagree. CI runs it.
- The initial plugin is v0, the plugin the repository root holds today. It is the default.
- Plugins remain loadable from a folder path, so an evaluation tool can load any plugin of
  the repository at a given commit without knowing its content.

## Capabilities

### New Capabilities
- `plugin-catalog`: the set of plugins in the repository, how each is enabled or loaded, the
  default plugin, plugin states and their transitions, evaluation status, and the consistency
  check.

### Modified Capabilities

## Impact

- Repository layout, `.claude-plugin/marketplace.json`, `README.md`, CI.
- Projects that enable `simplicity-rules@simplicity-rules`: none are known.
  job-search-agent enables no plugin today. It will enable the default plugin in a separate
  change in that repository.
- job-search-bench loads a plugin with `--plugin-dir <clone>`. After this change, the path
  names a plugin folder inside the clone. The bench change is made in that repository.
- job-search-bench results reference plugins by commit. They are rewritten to reference plugin
  folders. Until then, tags keep the two referenced commits reachable.
