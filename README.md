# simplicity-rules

A Claude Code plugin. It holds skills, hooks and agents that act during and after code
generation, and minimum tool versions. The current target is low cognitive complexity in
generated Python code.

Changes to the plugin are adopted on measured results: cognitive complexity, review effort
and review findings on real features.

## Layout

```
.claude-plugin/plugin.json       plugin manifest
.claude-plugin/marketplace.json  marketplace listing this plugin
skills/<name>/SKILL.md           skills, invoked as /simplicity-rules:<name>
hooks/hooks.json                 hooks
agents/<name>.md                 subagents
scripts/check-versions.sh        compares installed tools with versions.toml
versions.toml                    minimum tool versions
```

`main` holds the manifest only. Skills, hooks and agents arrive through adopted candidates.

## Requirements

- Claude Code at the version in `versions.toml` or newer. `scripts/check-versions.sh` checks it.
- Python code in the target project.
- Rootless podman for skills that run checkers in a container. The first run builds the
  image and needs network access.

## Use

### Install and enable per project

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

Update after a new `main`:

```
claude plugin marketplace update simplicity-rules
claude plugin update simplicity-rules@simplicity-rules
```

### Load for one session

```
claude --plugin-dir <path-to-simplicity-rules>
```

Nothing is written to `~/.claude`. The plugin loads from the directory as it is on disk.

## Evaluation

The plugin is tested on [csggnn/job-search-agent](https://github.com/csggnn/job-search-agent).
[job-search-bench](https://github.com/csggnn/job-search-bench) runs the evaluation.

`main` is the champion. A candidate change is a short-lived branch of this repo. The bench
implements the same real feature with each version of the plugin and compares the results.
An adopted candidate is merged to `main`. A rejected candidate is tagged
`setup-rejected/<idea>` and its branch is deleted.

## Development

Requires [uv](https://docs.astral.sh/uv/) and [Node.js](https://nodejs.org/), which provides
`npx`. Install the git hooks once:

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
Python with Ruff (`ruff.toml`), scan for secrets with gitleaks and audit workflows with zizmor.

- Dependabot updates the GitHub Actions weekly, after a 7-day cooldown.
- CodeRabbit reviews pull requests (`.coderabbit.yaml`).
- OpenSpec changes and specs live in `openspec/`.

## License

MIT
