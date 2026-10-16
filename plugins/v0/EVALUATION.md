State: default

# v0

## Goal and scope

Goal: baseline for comparisons. The plugin adds no skills, hooks or agents, so a session
with it behaves as a session without the repository.

Scope: any task, any language.

## Comparisons

| Comparison | Setup label | Role | Result summary |
| -- | -- | -- | -- |
| `2026-10-15-csg-57-commute-city-level-fallback-r3` | `v0` (X) | baseline against `cc-review` | 36 turns, 1.87 USD, cognitive total 125, blind checklist total 17. The judge preferred `cc-review` in 3 of 3 judge calls. |
| `2026-10-15-csg-57-commute-city-level-fallback-r3-noise` | `v0-a` (X), `v0-b` (Y) | two more runs of v0 | 40 and 57 turns, 1.97 USD each, cognitive total 122 and 126, blind checklist total 14 and 13. The judge preferred `v0-b` in 2 of 3 judge calls. |

## Assessment

Three agent runs of v0 on one task differ by up to 21 turns (36 to 57), 4 cognitive points
(122 to 126), 4 blind checklist points (13 to 17) and 0.10 USD (1.87 to 1.97). The judge
preferred one of two identical setups, `v0-b` over `v0-a`, in 2 of 3 judge calls. A difference
smaller than this range between v0 and another plugin on one task is not evidence of an
effect.

Open question: the noise range on a task other than `csg-57-commute-city-level-fallback`.

## Decision

Default plugin, kept as the baseline. 2026-10-16.
