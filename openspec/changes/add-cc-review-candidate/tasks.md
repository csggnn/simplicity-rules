# Tasks

## 1. Plugin folder

- [x] 1.1 Copy `rules.md`, `hooks/hooks.json`, `hooks/rules.sh` and the two skills from tag
  `plugins/cc-review-49412cc` into `plugins/sr-cc-review/`. Verify each copied file matches
  `git show plugins/cc-review-49412cc:<path>`, and `hooks/rules.sh` is executable.
- [x] 1.2 Create `plugins/sr-cc-review/.claude-plugin/plugin.json` from the tag's manifest
  with `"name": "sr-cc-review"` and a description of the goal and scope. Verify
  `claude plugin validate plugins/sr-cc-review` passes.
- [x] 1.3 In `plugins/sr-cc-review/rules.md`, replace the prefix `simplicity-rules:` with
  `sr-cc-review:`. Verify `grep -r "simplicity-rules:" plugins/sr-cc-review` finds nothing,
  the prefix equals the `name` in `plugins/sr-cc-review/.claude-plugin/plugin.json`, and the
  rest of `rules.md` matches the tag.
- [x] 1.4 Write `plugins/sr-cc-review/EVALUATION.md` as in design.md: `State: candidate`,
  Goal and scope, Comparisons with the figures from the job-search-bench summary of
  `2026-10-15-csg-57-commute-city-level-fallback-r3`, Assessment and Decision. Verify each
  figure against that summary.

## 2. Catalog and behavior

- [x] 2.1 Add `[plugins.sr-cc-review]` with `state = "candidate"` to `plugins.toml` and an
  `sr-cc-review` marketplace entry with `"source": "./plugins/sr-cc-review"` and a one-line
  `description`. Verify `python3 scripts/check-plugins.py`, `python3 -m unittest discover -s
  tests` and `claude plugin validate .` pass.
- [x] 2.2 Start a session with `claude --plugin-dir plugins/sr-cc-review` in a scratch Python
  project, change a function, and ask for a commit. Verify the session context holds the rule
  and the session runs `sr-cc-review:design-review` and `sr-cc-review:cognitive-complexity`.
  Repeat with a second `--plugin-dir` that points to a scratch plugin named `other`, with
  skills `design-review` and `cognitive-complexity` that each print a marker line. Verify the
  session runs the sr-cc-review skills and no `other:` skill.
- [x] 2.3 In a scratch `CLAUDE_CONFIG_DIR`, add the marketplace from the working tree. Verify
  `claude plugin install sr-cc-review@simplicity-rules` succeeds and reads from
  `plugins/sr-cc-review`, and `simplicity-rules@simplicity-rules` still reads from
  `plugins/sr-v0`. Add a second scratch marketplace with an entry named `simplicity-rules`
  and `"source"` set to `plugins/sr-cc-review`, and install it. Verify a session lists the
  skills as `sr-cc-review:design-review` and `sr-cc-review:cognitive-complexity`.

## 3. Checks

- [ ] 3.1 Run `uvx pre-commit run --all-files` and `openspec validate --all`. Verify both
  pass, and CI passes on the pull request.

## Workflow follow-up

- After the pull request is merged, delete `candidate/cognitive-complexity` on the remote and
  locally.
