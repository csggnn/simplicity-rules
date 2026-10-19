# simplicity-rules

A catalog of Claude Code plugins. See README.md for use and the procedures to change a
plugin's state.

## Plugin catalog rules

- Each plugin is a folder `plugins/<name>/` with `.claude-plugin/plugin.json` (`"name"` equals
  the folder name), `EVALUATION.md` and the plugin content.
- A plugin's `<name>` starts with `sr-`, e.g. `sr-v0`. Claude Code namespaces skills with the
  manifest `name`.
- `plugins.toml` records the state of every plugin and the default. Change a state there.
- A plugin has a marketplace entry named after its folder when its state is `candidate`,
  `default` or `opt-in`, and none when it is `archived`. Offered plugins have a one-line
  `description` of the goal and scope.
- A state change edits together: the state in `plugins.toml`, the first line and the Decision
  section of the plugin's `EVALUATION.md`, and the plugin's marketplace entry. A new default
  also edits `default` in `plugins.toml` and the `simplicity-rules` marketplace entry, which
  keeps `"strict": false`. README.md lists the steps.
- A change to one plugin does not edit the manifest or content of another plugin. A new
  default also edits the `EVALUATION.md` of the plugin it replaces.
- `versions.toml` and `scripts/check-versions.sh` are shared by all plugins.

## Check

```
python3 scripts/check-plugins.py
python3 -m unittest discover -s tests
uvx pre-commit run --all-files
```

`scripts/check-plugins.py` and its tests run as pre-commit hooks and in CI. A new rule in the
check needs a case in `tests/test_check_plugins.py`.
