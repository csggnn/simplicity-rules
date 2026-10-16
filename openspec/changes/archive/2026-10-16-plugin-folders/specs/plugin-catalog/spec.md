# Spec Delta

## Purpose

The set of Claude Code plugins this repository holds: how each plugin is loaded or enabled,
which one is the default, the state of each plugin and its evaluation status.

## ADDED Requirements

### Requirement: Plugins coexist and load independently
The repository SHALL hold each plugin in its own folder on the default branch. Each plugin
folder SHALL load with `claude --plugin-dir <folder>`. Several plugin folders SHALL load
together in one session. Loading a plugin SHALL NOT require a branch checkout.

#### Scenario: Load one plugin for a session
- **WHEN** the user runs `claude --plugin-dir <repository>/plugins/v0`
- **THEN** the session loads the v0 plugin

#### Scenario: Load two plugins together
- **WHEN** the user passes the folders of two plugins with two `--plugin-dir` options
- **THEN** the session loads both plugins

### Requirement: Each plugin has one state
Each plugin SHALL have exactly one state: `candidate`, `default`, `opt-in` or `archived`.
Exactly one plugin SHALL have the state `default`.

- `candidate`: under evaluation. Offered for installation.
- `default`: the plugin a project uses unless it chooses another. Offered for installation.
- `opt-in`: kept for use on request. Offered for installation.
- `archived`: deprecated and kept for reference. Not offered for installation.

#### Scenario: Initial states
- **WHEN** this change is applied
- **THEN** v0 is the only plugin, and its state is `default`

### Requirement: The marketplace offers every plugin that is not archived
Installing the repository's marketplace SHALL offer, by name, every plugin whose state is
`default`, `opt-in` or `candidate`, and no plugin whose state is `archived`. It SHALL also
offer an entry named `simplicity-rules` that installs the plugin whose state is `default`.

#### Scenario: Marketplace listing
- **WHEN** the user adds the marketplace and lists its plugins
- **THEN** the list holds `simplicity-rules` and `v0`

#### Scenario: Candidate offered
- **WHEN** a plugin has the state `candidate`
- **THEN** the marketplace lists it by name
- **AND** `claude --plugin-dir` loads it from its folder

### Requirement: A project can follow the default
A project that enables `simplicity-rules@simplicity-rules` SHALL get the plugin whose state is
`default` after a marketplace and plugin update, with no edit to the project. A project that
enables a plugin by its own name SHALL keep that plugin when the default changes.

#### Scenario: Default changes
- **WHEN** a project enables `simplicity-rules@simplicity-rules`, the default changes from v0
  to another plugin, and the user updates the marketplace and the plugin
- **THEN** the project loads the new default plugin

#### Scenario: Named plugin
- **WHEN** a project enables `v0@simplicity-rules` and the default changes to another plugin
- **THEN** the project keeps loading v0

### Requirement: State changes follow documented procedures
The repository documentation SHALL give the steps to add a candidate, to make a plugin the
default, to make a plugin opt-in, to archive a plugin and to delete a plugin. An archived
plugin SHALL keep its folder and evaluation status. A deleted plugin SHALL be recoverable from
git history.

#### Scenario: Archive a plugin
- **WHEN** the user follows the archive procedure for an opt-in plugin
- **THEN** the plugin's state is `archived`, the marketplace no longer offers it, and its
  folder and evaluation status remain in the repository

### Requirement: Each plugin states its goal and scope
Each plugin SHALL state its goal and its scope. The goal is what the plugin is meant to
achieve. The scope is the kinds of task it is meant for, such as task size, complexity or
programming language, and any kind it is not meant for. The marketplace entry of each offered
plugin SHALL carry a one-line summary of the goal and scope.

#### Scenario: Choosing a plugin
- **WHEN** the user lists the marketplace's plugins
- **THEN** each entry shows a one-line summary of the plugin's goal and scope

### Requirement: Each plugin states its evaluation status
Each plugin folder SHALL hold an evaluation status that states the plugin's state, its goal
and scope in full, the job-search-bench comparisons that evaluated it with their setup labels,
a summary of each comparison's result, an assessment, and the decision with its date. The
assessment states the cost and the benefit observed, the open questions and the next
experiment. A plugin with no evaluation SHALL state that it has none.

#### Scenario: Reading an evaluation status
- **WHEN** the user reads v0's evaluation status
- **THEN** it states the state `default`, its goal and scope, and the comparisons that used it
  as the baseline

### Requirement: A check enforces consistency
A repository check SHALL fail when:

- a plugin has no state, or a state names no plugin folder,
- the number of `default` plugins is not one,
- the marketplace offers an `archived` plugin, or omits a `default`, `opt-in` or `candidate`
  plugin,
- the marketplace lists a plugin name more than once,
- the recorded default plugin does not have the state `default`,
- the `simplicity-rules` entry does not install the `default` plugin,
- a plugin folder lacks its manifest or its evaluation status,
- the marketplace entry of an offered plugin has no description,
- a plugin's evaluation status states a different state than the one recorded.

CI SHALL run the check on pull requests and on pushes to the default branch.

#### Scenario: Default points at an archived plugin
- **WHEN** the recorded default plugin has the state `archived`
- **THEN** the check fails and names the plugin

#### Scenario: Consistent repository
- **WHEN** the states, the marketplace, the folders and the evaluation statuses agree
- **THEN** the check passes
