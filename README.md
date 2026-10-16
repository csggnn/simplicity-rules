# simplicity-rules

A catalog of Claude Code plugins. Each plugin holds skills, hooks and agents that act during
and after code generation. The current target is low cognitive complexity in generated Python
code.

Changes are adopted on measured results: cognitive complexity, review effort and review
findings on real features.

## Layout

```
.claude-plugin/marketplace.json   plugins offered for installation
plugins.toml                      state of every plugin
plugins/<name>/
  .claude-plugin/plugin.json      manifest, "name" equals <name>
  EVALUATION.md                   goal, scope, comparisons, assessment, decision
  skills/, hooks/, agents/, ...   plugin content
scripts/check-versions.sh         compares installed tools with versions.toml
scripts/check-plugins.py          checks that plugins.toml, the folders and the marketplace agree
versions.toml                     minimum tool versions
```

## Plugins

`plugins.toml` records the state of every plugin. The marketplace lists each offered plugin
with a one-line goal and scope. `plugins/<name>/EVALUATION.md` holds the state, goal, scope,
comparisons, assessment and decision of a plugin.

### States

| State | Meaning | Listed in the marketplace |
| -- | -- | -- |
| `candidate` | Under evaluation. | yes |
| `default` | The plugin a project uses unless it chooses another. Exactly one. | yes |
| `opt-in` | Kept for use on request. | yes |
| `archived` | Deprecated and kept for reference. | no |

`plugins.toml` records the state of every plugin. The marketplace entry `simplicity-rules`
installs the default plugin.

## Requirements

- Claude Code at the version in `versions.toml` or newer. `scripts/check-versions.sh` checks
  the installed versions.
- Python code in the target project.
- [uv](https://docs.astral.sh/uv/) at the version in `versions.toml` or newer. Skills run
  checkers with `uvx` at pinned versions. The first run of a checker downloads it.

## Use

### Follow the default in a project

Commit this to the project's `.claude/settings.json`. Claude Code offers to install the
marketplace and the plugin when the project is trusted.

```
{
  "extraKnownMarketplaces": {
    "simplicity-rules": { "source": { "source": "github", "repo": "csggnn/simplicity-rules" } }
  },
  "enabledPlugins": { "simplicity-rules@simplicity-rules": true }
}
```

The project loads a new default after `claude plugin marketplace update simplicity-rules` and
`claude plugin update simplicity-rules@simplicity-rules`.

### Install per user

```
claude plugin marketplace add csggnn/simplicity-rules
claude plugin install simplicity-rules@simplicity-rules
```

Installing copies the plugin into `~/.claude/plugins/`. Enable it for one project in that
project's `.claude/settings.local.json`:

```
{
  "enabledPlugins": { "simplicity-rules@simplicity-rules": true }
}
```

To use a specific plugin and keep it when the default changes, install and enable
`<name>@simplicity-rules`, for example `v0@simplicity-rules`. Enable either
`simplicity-rules@simplicity-rules` or a named plugin, not both, so the same plugin does not
load twice.

### Load for one session

```
claude --plugin-dir <path-to-simplicity-rules>/plugins/<name>
```

The option repeats to load several plugins in one session. Nothing is written to `~/.claude`.
A plugin loads from its folder as it is on disk, in any state.

### Permissions

Skills run checkers as `uvx <checker>==<version> ...`. Claude Code asks before each run
unless the project or user settings allow it. A rule names the pinned version, e.g.
`"allow": ["Bash(uvx complexipy==8.0.1:*)"]`.

## Change a plugin's state

A plugin has a marketplace entry named after its folder when its state is `candidate`,
`default` or `opt-in`, and none when it is `archived`. A state change edits together:

- the state in `plugins.toml`,
- the first line of the plugin's `EVALUATION.md`, and the date and decision in its Decision
  section,
- the plugin's marketplace entry, added or removed as above,
- for a new default: `default` in `plugins.toml` and the `simplicity-rules` marketplace entry.

Each procedure ends with:

```
python3 scripts/check-plugins.py
claude plugin validate .
```

`scripts/check-plugins.py` also runs in pre-commit and CI.

### Add a candidate

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json` (`"name": "<name>"`) and the
   plugin content.
2. Create `plugins/<name>/EVALUATION.md` starting with `State: candidate`, with the sections
   Goal and scope, Comparisons, Assessment and Decision.
3. Add `[plugins.<name>]` with `state = "candidate"` to `plugins.toml`.
4. Add an entry named `<name>` with `"source": "./plugins/<name>"` and a one-line
   `description` of the goal and scope to `.claude-plugin/marketplace.json`.

### Make a plugin the default

1. In `plugins.toml`, set `default = "<name>"`, set the state of `<name>` to `default` and set
   the previous default to `opt-in` or `archived`.
2. Update the first line and the Decision section of both `EVALUATION.md` files.
3. If `<name>` was `archived`, add its marketplace entry. If the previous default is now
   `archived`, remove its marketplace entry.
4. In the `simplicity-rules` marketplace entry, set `source` to `./plugins/<name>`, update the
   `description`, and keep `"strict": false`. The entry shares its source with the named entry.

### Make a plugin opt-in

The plugin must not be the default. To demote the default, make another plugin the default
with the procedure above, which sets the previous default to `opt-in`.

1. Set the state to `opt-in` in `plugins.toml`.
2. Update the first line and the Decision section of its `EVALUATION.md`.
3. If the plugin was `archived`, add its marketplace entry.

### Archive a plugin

The plugin must not be the default.

1. Set the state to `archived` in `plugins.toml`.
2. Update the first line and the Decision section of its `EVALUATION.md`.
3. Remove its marketplace entry. The folder stays in `plugins/`.

### Delete a plugin

The plugin must not be the default. Remove `plugins/<name>/`, its `[plugins.<name>]` table and
its marketplace entry. The plugin stays recoverable from git history.

## Evaluation

The plugins are tested on [csggnn/job-search-agent](https://github.com/csggnn/job-search-agent).
[job-search-bench](https://github.com/csggnn/job-search-bench) runs the evaluation. The bench
implements the same real feature with each plugin under comparison and compares the results.
It loads a plugin with `--plugin-dir <clone>/plugins/<name>`.

A new idea is a candidate plugin. The result of its comparisons goes into its `EVALUATION.md`.
An adopted candidate becomes the default or opt-in. A rejected candidate is archived or
deleted.

## Development

Requires [uv](https://docs.astral.sh/uv/), [Node.js](https://nodejs.org/), which provides
`npx`, and Python 3.11 or newer, which runs `scripts/check-plugins.py`. Install the git hooks once:

```
uvx pre-commit install
```

Run all local checks:

```
uvx pre-commit run --all-files
npx --yes @fission-ai/openspec@1.14.2 validate --all --no-interactive
```

CI (`.github/workflows/ci.yml`) runs both on pushes to `main` and on pull requests. The hooks
check whitespace, YAML, TOML and JSON, lint shell scripts with shellcheck, lint and format
Python with Ruff (`ruff.toml`), scan for secrets with gitleaks, audit workflows with zizmor
check the plugin catalog with `scripts/check-plugins.py` and run its tests in `tests/`
(`python3 -m unittest discover -s tests`).

- Dependabot updates the GitHub Actions weekly, after a 7-day cooldown.
- CodeRabbit reviews pull requests (`.coderabbit.yaml`).
- OpenSpec changes and specs live in `openspec/`.

## License

MIT
