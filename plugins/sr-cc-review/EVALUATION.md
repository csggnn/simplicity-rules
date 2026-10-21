State: candidate

# sr-cc-review

## Goal and scope

Goal: lower cognitive complexity and better module design in Python code that Claude Code
writes. At session start the plugin adds a rule: before committing changed Python code, run
`sr-cc-review:design-review` and then `sr-cc-review:cognitive-complexity` on it.

Scope: Python features that span several functions or modules. Not meant for trivial
changes, where it adds effort with no measured gain, or for other languages.

## Comparisons

| Comparison | Setup label | Role | Result summary |
| -- | -- | -- | -- |
| `2026-10-15-csg-57-commute-city-level-fallback-r3` | `cc-review` (Y) | candidate against `v0` (X) | 81 turns, 3.59 USD, cognitive total 129, blind checklist total 12. The judge preferred `cc-review` in 3 of 3 judge calls. |

## Assessment

sr-cc-review used more effort than sr-v0: 81 turns and 3.59 USD against 36 to 57 turns and
1.87 to 1.97 USD over three sr-v0 runs. Its cognitive total of 129 is above the sr-v0 range
of 122 to 126. Its blind checklist total of 12 is below the sr-v0 range of 13 to 17. The
judge preferred it in 3 of 3 judge calls. The improvement is qualitative and limited.

Open question: the effect on a more complex task.

Next experiment: a comparison with sr-v0 on such a task.

## Decision

Kept as a candidate. 2026-10-16.
