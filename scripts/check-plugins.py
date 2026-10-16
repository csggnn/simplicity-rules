#!/usr/bin/env python3
"""Check that plugins.toml, the plugin folders and the marketplace agree.

Prints one line per violation. Exit status is 1 when there is any.
"""

import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATES = {"candidate", "default", "opt-in", "archived"}
OFFERED_STATES = STATES - {"archived"}
ALIAS = "simplicity-rules"


def load_states(errors):
    data = tomllib.loads((ROOT / "plugins.toml").read_text())
    states = {}
    for name, entry in data.get("plugins", {}).items():
        state = entry.get("state")
        if state not in STATES:
            errors.append(f"{name}: state {state!r} is not one of {sorted(STATES)}")
        states[name] = state
    return data.get("default"), states


def check_folders(states, errors):
    folders = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir()}
    for name in sorted(folders - states.keys()):
        errors.append(f"{name}: folder has no state in plugins.toml")
    for name in sorted(states.keys() - folders):
        errors.append(f"{name}: state names no folder in plugins/")
    for name in sorted(folders & states.keys()):
        check_folder(name, states[name], errors)


def check_folder(name, state, errors):
    folder = ROOT / "plugins" / name
    manifest = folder / ".claude-plugin" / "plugin.json"
    if not manifest.is_file():
        errors.append(f"{name}: missing .claude-plugin/plugin.json")
    elif json.loads(manifest.read_text()).get("name") != name:
        errors.append(f"{name}: manifest name differs from the folder name")
    evaluation = folder / "EVALUATION.md"
    if not evaluation.is_file():
        errors.append(f"{name}: missing EVALUATION.md")
        return
    first_line = evaluation.read_text().splitlines()[0]
    if first_line != f"State: {state}":
        errors.append(f"{name}: EVALUATION.md starts {first_line!r}, recorded state is {state!r}")


def check_default(default, states, errors):
    defaults = sorted(n for n, s in states.items() if s == "default")
    if len(defaults) != 1:
        errors.append(f"plugins.toml: {len(defaults)} plugins have the state default: {defaults}")
    elif default != defaults[0]:
        errors.append(
            f"plugins.toml: default is {default!r}, the plugin in state default is {defaults[0]!r}"
        )


def check_marketplace(default, states, errors):
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    entries = {e["name"]: e for e in marketplace.get("plugins", [])}
    for name, entry in entries.items():
        if not entry.get("description"):
            errors.append(f"{name}: marketplace entry has no description")
        if name == ALIAS:
            expected = f"./plugins/{default}"
        elif name in states:
            expected = f"./plugins/{name}"
        else:
            errors.append(f"{name}: marketplace entry names no plugin")
            continue
        if entry.get("source") != expected:
            errors.append(
                f"{name}: marketplace source is {entry.get('source')!r}, expected {expected!r}"
            )
        if name != ALIAS and states[name] not in OFFERED_STATES:
            errors.append(f"{name}: state is {states[name]}, the marketplace offers it")
    for name, state in states.items():
        if state in OFFERED_STATES and name not in entries:
            errors.append(f"{name}: state is {state}, the marketplace omits it")
    if ALIAS not in entries:
        errors.append(f"{ALIAS}: marketplace has no {ALIAS} entry")


def main():
    errors = []
    default, states = load_states(errors)
    check_folders(states, errors)
    check_default(default, states, errors)
    check_marketplace(default, states, errors)
    print("\n".join(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
