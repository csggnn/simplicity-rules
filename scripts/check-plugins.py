#!/usr/bin/env python3
"""Check that plugins.toml, the plugin folders and the marketplace agree.

Requires Python 3.11 or newer. Prints one line per violation. Exit status is 1 when there is any.
"""

import json
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    sys.exit("check-plugins.py requires Python 3.11 or newer")

ROOT = Path(__file__).resolve().parent.parent
STATES = {"candidate", "default", "opt-in", "archived"}
OFFERED_STATES = STATES - {"archived"}
ALIAS = "simplicity-rules"


def read(path, parse, errors):
    """Return the parsed file, or None after recording why it could not be read."""
    try:
        return parse(path.read_text())
    except (OSError, ValueError) as error:
        errors.append(f"{path.relative_to(ROOT)}: cannot read: {error}")
        return None


def load_states(errors):
    data = read(ROOT / "plugins.toml", tomllib.loads, errors) or {}
    states = {}
    for name, entry in data.get("plugins", {}).items():
        state = entry.get("state") if isinstance(entry, dict) else None
        if state not in STATES:
            errors.append(f"{name}: state {state!r} is not one of {sorted(STATES)}")
        states[name] = state
    return data.get("default"), states


def check_folders(states, errors):
    plugins = ROOT / "plugins"
    if not plugins.is_dir():
        errors.append("plugins: folder is missing")
        return
    folders = {p.name for p in plugins.iterdir() if p.is_dir()}
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
    else:
        data = read(manifest, json.loads, errors)
        if data is not None and (not isinstance(data, dict) or data.get("name") != name):
            errors.append(f"{name}: manifest name differs from the folder name")
    evaluation = folder / "EVALUATION.md"
    if not evaluation.is_file():
        errors.append(f"{name}: missing EVALUATION.md")
        return
    text = read(evaluation, str, errors)
    first_line = (text or "").splitlines()[:1]
    if first_line != [f"State: {state}"]:
        found = first_line[0] if first_line else ""
        errors.append(f"{name}: EVALUATION.md starts {found!r}, recorded state is {state!r}")


def check_default(default, states, errors):
    if default not in states:
        errors.append(f"plugins.toml: default {default!r} names no plugin")
    elif states[default] != "default":
        errors.append(f"{default}: recorded as the default but its state is {states[default]}")
    defaults = sorted(n for n, s in states.items() if s == "default")
    if len(defaults) != 1:
        errors.append(f"plugins.toml: {len(defaults)} plugins have the state default: {defaults}")


def check_entry(name, entry, default, states, errors):
    if not entry.get("description"):
        errors.append(f"{name}: marketplace entry has no description")
    if name == ALIAS:
        expected = f"./plugins/{default}"
        if entry.get("strict") is not False:
            errors.append(f"{name}: marketplace entry must set strict to false")
    elif name in states:
        expected = f"./plugins/{name}"
        if states[name] not in OFFERED_STATES:
            errors.append(f"{name}: state is {states[name]}, the marketplace offers it")
    else:
        errors.append(f"{name}: marketplace entry names no plugin")
        return
    if entry.get("source") != expected:
        errors.append(
            f"{name}: marketplace source is {entry.get('source')!r}, expected {expected!r}"
        )


def marketplace_entries(errors):
    """Return the marketplace entries by name, recording duplicates and malformed entries."""
    path = ROOT / ".claude-plugin" / "marketplace.json"
    marketplace = read(path, json.loads, errors)
    listed = marketplace.get("plugins", []) if isinstance(marketplace, dict) else []
    entries = {}
    for entry in listed:
        name = entry.get("name") if isinstance(entry, dict) else None
        if not isinstance(name, str):
            errors.append(f"marketplace entry without a name: {entry!r}")
        elif name in entries:
            errors.append(f"{name}: marketplace lists this name more than once")
        else:
            entries[name] = entry
    return entries


def check_marketplace(default, states, errors):
    entries = marketplace_entries(errors)
    for name, entry in entries.items():
        check_entry(name, entry, default, states, errors)
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
