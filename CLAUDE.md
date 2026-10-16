# simplicity-rules

A catalog of Claude Code plugins. See README.md for use and the procedures to change a
plugin's state.

## Plugin catalog rules

- Each plugin is a folder `plugins/<name>/` with `.claude-plugin/plugin.json` (`"name"` equals
  the folder name), `EVALUATION.md` and the plugin content.
- `plugins.toml` records the state of every plugin and the default. Change a state there.
- A state change edits four places together: `plugins.toml`, the first line of the plugin's
  `EVALUATION.md`, the plugin's entry in `.claude-plugin/marketplace.json` and, for the
  default, the `simplicity-rules` entry in `.claude-plugin/marketplace.json`.
- Offered plugins (`default`, `opt-in`, `candidate`) have a marketplace entry with a one-line
  `description` of the goal and scope. `archived` plugins have none.
- A change to one plugin does not edit another plugin's folder.
- `versions.toml` and `scripts/check-versions.sh` are shared by all plugins.

## Check

```
python3 scripts/check-plugins.py
uvx pre-commit run --all-files
```

`scripts/check-plugins.py` runs as a pre-commit hook and in CI.
