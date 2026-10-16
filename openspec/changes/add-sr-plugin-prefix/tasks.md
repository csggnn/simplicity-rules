# Tasks

## 1. Rename v0 to sr-v0

- [ ] 1.1 Move `plugins/v0/` to `plugins/sr-v0/` and set `"name": "sr-v0"` in its manifest.
  Verify `claude plugin validate plugins/sr-v0` passes.
- [ ] 1.2 In `plugins/sr-v0/EVALUATION.md`, name the plugin `sr-v0`. Keep the setup labels.
  Verify the first line reads `State: default`.
- [ ] 1.3 In `plugins.toml`, set `default = "sr-v0"` and rename the table to
  `[plugins.sr-v0]`. In `.claude-plugin/marketplace.json`, rename the entry `v0` to `sr-v0`,
  set both sources to `./plugins/sr-v0` and name `sr-v0` in the `simplicity-rules`
  description. Verify `python3 scripts/check-plugins.py` and `claude plugin validate .` pass.

## 2. Consistency check

- [ ] 2.1 In `scripts/check-plugins.py`, report every plugin name in `plugins.toml` or folder
  in `plugins/` that does not start with `sr-`. Add a case to `tests/test_check_plugins.py`
  with an archived plugin `old` that has a folder, a manifest and an evaluation status.
  Rename the existing cases to `sr-v0`. Verify `python3 -m unittest discover -s tests` passes.

## 3. Documentation

- [ ] 3.1 State the prefix in `README.md` (layout and Add a candidate) and `CLAUDE.md`, and
  use `sr-v0` in the examples. Verify `grep -rn "v0" README.md CLAUDE.md` finds only `sr-v0`.

## 4. Checks

- [ ] 4.1 Run `python3 scripts/check-plugins.py`, `python3 -m unittest discover -s tests`,
  `uvx pre-commit run --all-files`, `openspec validate --all`, `claude plugin validate .` and
  `claude plugin validate plugins/sr-v0`. Verify each passes.
