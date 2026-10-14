# simplicity-rules

Tools and guidance for coding agents. It holds Claude Code guidance and minimum tool
versions. A project consumes it as the git submodule `.setup/`, pinned to a commit.

The current target is low cognitive complexity in generated Python code. Changes to the
setup are adopted on measured results: cognitive complexity, review effort and review
findings on real features.

## Test project

The setup is tested on [csggnn/job-search-agent](https://github.com/csggnn/job-search-agent).
[job-search-bench](https://github.com/csggnn/job-search-bench) runs the evaluation
([spec](https://github.com/csggnn/job-search-agent/issues/84)).

`main` is the champion setup. A candidate change is a short-lived branch of this repo. The
bench evaluates it against `main` by implementing the same real feature in
job-search-agent with each setup. An adopted candidate is merged to `main`. A rejected
candidate is tagged `setup-rejected/<idea>` and its branch is deleted.

## Target project requirements

- Python code.
- Claude Code as the coding agent, at the version in `versions.toml` or newer.

## Integration

Run from the target project root.

1. Add the submodule:

   ```
   git submodule add https://github.com/csggnn/simplicity-rules.git .setup
   ```

2. Check tool versions:

   ```
   .setup/scripts/check-versions.sh
   ```

3. Import the generic rules. Add this line to the project `CLAUDE.md`, after the title:

   ```
   @.setup/CLAUDE.generic.md
   ```

4. Allow the setup scripts and block agent edits to the setup. Project
   `.claude/settings.json`:

   ```
   {
     "permissions": {
       "allow": ["Bash(.setup/scripts/*)"],
       "deny": ["Edit(.setup/**)"]
     }
   }
   ```

   An `Edit` rule covers every file-editing tool.

5. Check out the submodule in CI: `actions/checkout` with `submodules: true`.

6. Commit `.gitmodules`, `.setup`, `CLAUDE.md` and `.claude/settings.json`.

A fresh clone of the project needs `git submodule update --init`.

### Update to a new setup commit

```
git -C .setup fetch && git -C .setup checkout <sha>
git add .setup
```

## Project layer

The project keeps everything specific to it: its `CLAUDE.md` rules and invariants, lint
configuration, CI workflows, skills, PR templates and permission settings.

## License

MIT
