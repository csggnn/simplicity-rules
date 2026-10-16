# Spec Delta

## Purpose

What the cc-review plugin does in a Claude Code session: a rule given at session start, a
design review skill and a cognitive complexity skill, applied to changed Python code before
it is committed.

## ADDED Requirements

### Requirement: The session starts with the review rule
When a session starts with cc-review loaded, the session context SHALL contain a rule: after
writing or changing Python code and before committing it, run the design review and then the
cognitive complexity check on the changed code.

#### Scenario: Session start
- **WHEN** a session starts with cc-review loaded
- **THEN** the session context contains the rule naming the design review and the cognitive
  complexity check, in that order

### Requirement: The rule names the cc-review skills under any install name
The rule SHALL name the two skills of cc-review so that a session finds them whether
cc-review is installed as `cc-review@simplicity-rules`, installed as
`simplicity-rules@simplicity-rules` while it is the default, or loaded from its folder. The
names SHALL NOT match a skill of another loaded plugin.

#### Scenario: Loaded from its folder
- **WHEN** a session loads cc-review with `--plugin-dir` and Python code changes
- **THEN** the session runs both skills named in the rule

#### Scenario: Another plugin defines skills with the same names
- **WHEN** a session also loads a plugin with skills `design-review` and
  `cognitive-complexity`, and Python code changes
- **THEN** the session runs the cc-review skills and not the other plugin's skills

#### Scenario: Installed under the default entry
- **WHEN** cc-review is installed through a marketplace entry named `simplicity-rules`
- **THEN** the skills named in the rule exist in the session

### Requirement: The design review covers the session's changes
The design review skill SHALL review the code added or modified in the session, tests
included, for three principles: deep modules, information hiding and obvious code. It SHALL
fix each finding in that code, and list a finding in code the session does not touch without
changing that code. It SHALL report each finding with its file, function, principle and
action.

#### Scenario: Finding outside the session's changes
- **WHEN** the review finds a red flag in a function the session did not change
- **THEN** the report lists it as out of scope and the function is unchanged

### Requirement: The cognitive complexity check limits changed functions
The cognitive complexity skill SHALL measure the Python functions added or modified in the
session with a pinned version of a cognitive complexity checker. Each changed function SHALL
score 15 or less after the skill runs, or the report SHALL state why it does not. A refactor
SHALL NOT change behavior. A function above 15 that the session does not touch SHALL be
listed and left unchanged.

#### Scenario: Changed function above the limit
- **WHEN** a function changed in the session scores above 15
- **THEN** the skill refactors it, runs the tests that cover it, and reports the score before
  and after

#### Scenario: No Python change
- **WHEN** no Python file changed in the session
- **THEN** the skill reports it and measures nothing
