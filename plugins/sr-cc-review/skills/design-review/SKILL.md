---
name: design-review
description: Review the code added or modified in this session for shallow modules, information leakage and non-obvious code, and improve it before committing.
---

Review the code added or modified in this session against three principles, and fix each
finding in that code.

# Scope

The code under review is the code added or modified in this session, tests included. A
finding in code the session does not touch is out of scope: list it in the report and leave
the code unchanged.

The feature description (spec, design, tasks) is anchored, not fixed. A finding can come
from a decision in the description, such as a prescribed function signature. When changing
that decision makes the code simpler and keeps the feature's purpose, change the code and
the description files together.

# Principles

## 1. Deep modules

A function, class or module hides a substantial implementation behind a small interface.

Red flags:

- Callers combine several functions in a fixed sequence to do one job.
- A function's interface is as complex as its body, e.g. a wrapper around one call.
- A function mixes levels of abstraction, e.g. receives one input already resolved and
  resolves another input itself.

Fix: merge the functions into one function named after the job. Keep its helpers private.

## 2. Information hiding

Each design decision lives in one module.

Red flags:

- The vocabulary of an external system, such as API field names, codes or formats, appears
  outside the code that calls that system.
- One decision is applied in two places, e.g. an input format cleaned in two functions, or a
  constant imported to restate its value in another module.
- Callers compare a return value against a sentinel, or a function returns values of
  several types.
- Tests patch functions of the module under test.

Fix: move the decision into one module. Return a result that carries what callers need.
Patch only external boundaries in tests, such as HTTP clients and LLM calls.

## 3. Obvious code

A reader understands a function from its names and structure, without reading other code.

Red flags:

- A condition tests one variable and returns another, or depends on an invariant that the
  code does not state.
- The meaning of a call depends on positional values, e.g. `f(None, x, None)`.
- String literals serve as an enumeration.
- A name no longer matches its value, e.g. `raw_minutes` that includes a penalty.
- A docstring restates the code step by step.

Fix: name the case with a function or a keyword argument, use constants or an `Enum`,
rename, or make the invariant explicit in code.

# Procedure

1. Read the session's changes with `git diff` and `git status --short`, each run as a
   single command.
2. For each principle, list the findings: file, function, red flag, fix.
3. Apply the fixes that are in scope.
4. Run the tests that cover the changed code.

# Report

A table with one row per finding: file, function, principle, finding, action. The action is
`fixed`, `out of scope` or `description changed`. Then each description change, with the
reason.
