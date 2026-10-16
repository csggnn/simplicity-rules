# Design

## Context

See proposal.md for motivation and the specs for the required behavior.

- The catalog holds one plugin, v0, in `plugins/v0`. `plugins.toml`, the marketplace and
  `scripts/check-plugins.py` follow the layout and procedures in README.md.
- Commit `49412cc` on `candidate/cognitive-complexity` holds cc-review at the repository
  root: `.claude-plugin/plugin.json` named `simplicity-rules`, `rules.md`, `hooks/hooks.json`
  with a SessionStart hook that runs `hooks/rules.sh`, and the skills
  `skills/cognitive-complexity/SKILL.md` and `skills/design-review/SKILL.md`. The tag
  `plugins/cc-review-49412cc` points at that commit.
- `rules.md` names the skills `simplicity-rules:design-review` and
  `simplicity-rules:cognitive-complexity`. Claude Code namespaces a plugin's skills with the
  `name` in its `plugin.json`. A marketplace entry with a different `name` sets the name in
  `enabledPlugins`, not the namespace (plugins reference, "Metadata precedence").
- `hooks/rules.sh` prints `rules.md`, found relative to the script.
- job-search-bench comparison `2026-10-15-csg-57-commute-city-level-fallback-r3` ran
  cc-review as setup `cc-review` against v0. Its summary holds the turns, cost, cognitive
  complexity, blind checklist and judge results.

## Goals / Non-Goals

**Goals:**
- The skill and hook content is the content of `49412cc`, except where a plugin name in it
  stops being true. A later bench run on the folder measures the plugin the earlier run
  measured.
- No file outside `plugins/cc-review` changes except the catalog files the README's "Add a
  candidate" procedure edits.

**Non-Goals:**
- Changes to the skills' instructions, limits or checker version.
- Making cc-review the default or opt-in.

## Decisions

### Copy the plugin from the tag into `plugins/cc-review`

```
plugins/cc-review/
  .claude-plugin/plugin.json      "name": "cc-review"
  EVALUATION.md
  rules.md
  hooks/hooks.json, hooks/rules.sh
  skills/cognitive-complexity/SKILL.md
  skills/design-review/SKILL.md
```

The files come from `git show plugins/cc-review-49412cc:<path>`. `hooks/rules.sh` keeps its
executable bit. The root `versions.toml` already holds the `claude` and `uv` minimums the
skills need.

Alternative: merge the branch and move the files. Rejected because the branch's root layout
conflicts with the catalog layout, and the merge brings no history the tag does not keep.

### The rule names the skills with the manifest name

`plugins/cc-review/rules.md` names the skills `cc-review:design-review` and
`cc-review:cognitive-complexity`. The prefix is the `name` in
`plugins/cc-review/.claude-plugin/plugin.json`. It is the same when cc-review is installed as
`cc-review@simplicity-rules`, installed as `simplicity-rules@simplicity-rules` while it is
the default, or loaded with `--plugin-dir`. Task 2.2 verifies the skills run when another
loaded plugin defines skills with the same unprefixed names. Task 2.3 verifies the namespace
under a marketplace entry named `simplicity-rules`.

Alternative: name the skills without a prefix. Rejected because an unprefixed name also
matches a skill of the same name in another loaded plugin.

Alternative: generate the rule in `hooks/rules.sh` with the plugin name. Rejected because
the name is fixed in the manifest, and hooks receive no variable that holds it.

### Evaluation status

`plugins/cc-review/EVALUATION.md` starts with `State: candidate`.

- Goal and scope: lower cognitive complexity and better module design in Python code that
  Claude Code writes. Meant for Python features that span several functions or modules. Not
  meant for trivial changes, where it adds effort with no measured gain, or for other
  languages.
- Comparisons: `2026-10-15-csg-57-commute-city-level-fallback-r3`, setup `cc-review` (Y)
  against `v0` (X), with the figures from the comparison summary.
- Assessment: more effort than v0 (81 turns and 3.59 USD against 36 to 57 turns and 1.87 to
  1.97 USD over three v0 runs). Cognitive total 129, above the v0 range of 122 to 126. Blind
  checklist total 12 against 13 to 17. The judge preferred cc-review in 3 of 3 judge calls.
  The improvement is qualitative and limited. Open question: the effect on a more complex
  task. Next experiment: a comparison with v0 on such a task.
- Decision: kept as a candidate, 2026-10-16.

The marketplace `description` summarizes the goal and scope in one line.

### Branch deletion after merge

After the pull request is merged, `candidate/cognitive-complexity` is deleted on the remote
and locally. The tag keeps `49412cc` reachable until the saved bench results reference
plugin folders.

## Risks / Trade-offs

- [Renaming the manifest changes the skill names the rule must use] → The rule and the
  manifest name are in the same plugin folder. Task 1.3 checks they match.
- [The rule wording change alters the plugin's behavior compared with `49412cc`] → The change
  replaces the prefix only. A bench run on the folder can be compared with the `49412cc`
  results to confirm.
