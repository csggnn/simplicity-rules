---
name: cognitive-complexity
description: Measure the cognitive complexity of the Python functions changed on the current branch and refactor each one above the limit.
---

Measure the cognitive complexity of changed Python code and bring each changed function to
the limit or below.

# Limit

A function scores 15 or less.

# Files

If the request names paths, measure those. Otherwise measure the Python files changed on
the branch, committed or not:

1. Resolve the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`. If
   that fails, use the local branch `main`, or `master` when `main` does not exist.
2. `git diff --name-only --diff-filter=d $(git merge-base HEAD <default-branch>) -- '*.py'`
3. `git ls-files --others --exclude-standard -- '*.py'`

If no Python file changed, report it and stop.

# Measure

Run from the project root:

```
uvx complexipy==8.0.1 <files> --plain --sort desc --color no
```

Each output line is `<file> <function> <score>`. Exit status 1 means at least one function
in the measured files scores above 15.

The changed functions are the functions the branch adds or modifies, read from the diff.
A function above 15 that the branch does not touch is out of scope. List it in the report.

# Refactor

For each changed function above 15:

- Return early for edge cases and errors, so the main path is not nested.
- Move a nested block with a single purpose into a function named after that purpose.
- Replace a chain of conditions that maps an input to a value with a lookup table.
- Split a function that performs several steps in sequence into one function per step.
- Merge conditions that lead to the same action into one condition.

An extracted function has one purpose that its name states. A refactor does not change
behavior. Do not split a function at an arbitrary point to lower its score.

After refactoring, run the tests that cover the changed code, then measure again. Repeat
until each changed function scores 15 or less.

# Report

The default branch used, when step 1 ran. A table with one row per changed function: file, function, score before, score after.
Then each out-of-scope function above 15, and each changed function that still scores above
15 with the reason.
