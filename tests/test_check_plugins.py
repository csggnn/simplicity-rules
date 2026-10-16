"""Tests for scripts/check-plugins.py.

Each case copies the catalog files to a temporary folder, applies one fault and runs the check
there. Run with: python3 -m unittest discover -s tests
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATALOG = ("plugins", "plugins.toml", ".claude-plugin", "scripts")


def edit_marketplace(root, change):
    path = root / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text())
    change(data["plugins"])
    path.write_text(json.dumps(data))


def replace_in(root, relative, old, new):
    path = root / relative
    path.write_text(path.read_text().replace(old, new))


def archive_sr_v0(root):
    replace_in(root, "plugins.toml", 'state = "default"', 'state = "archived"')


def omit_sr_v0(root):
    edit_marketplace(root, lambda plugins: plugins.pop(1))


def list_archived_plugin_without_folder(root):
    with (root / "plugins.toml").open("a") as file:
        file.write('\n[plugins.sr-old]\nstate = "archived"\n')
    entry = {"name": "sr-old", "source": "./plugins/sr-old", "description": "x"}
    edit_marketplace(root, lambda plugins: plugins.append(entry))


def add_plugin_without_prefix(root):
    with (root / "plugins.toml").open("a") as file:
        file.write('\n[plugins.old]\nstate = "archived"\n')
    folder = root / "plugins" / "old"
    (folder / ".claude-plugin").mkdir(parents=True)
    (folder / ".claude-plugin" / "plugin.json").write_text('{"name": "old"}')
    (folder / "EVALUATION.md").write_text("State: archived\n")


def drop_description(root):
    edit_marketplace(root, lambda plugins: plugins[1].pop("description"))


def duplicate_sr_v0(root):
    edit_marketplace(root, lambda plugins: plugins.append(dict(plugins[1])))


def point_alias_elsewhere(root):
    edit_marketplace(root, lambda plugins: plugins[0].update(source="./plugins/other"))


def drop_strict(root):
    edit_marketplace(root, lambda plugins: plugins[0].pop("strict"))


def change_evaluation_state(root):
    replace_in(root, "plugins/sr-v0/EVALUATION.md", "State: default", "State: opt-in")


def empty_evaluation(root):
    (root / "plugins/sr-v0/EVALUATION.md").write_text("")


def break_marketplace_json(root):
    (root / ".claude-plugin" / "marketplace.json").write_text("{")


def break_manifest_json(root):
    (root / "plugins/sr-v0/.claude-plugin/plugin.json").write_text("{")


def add_unnamed_entry(root):
    edit_marketplace(root, lambda plugins: plugins.append({"source": "x"}))


def make_entry_not_a_table(root):
    (root / "plugins.toml").write_text('default = "sr-v0"\nplugins.sr-v0 = "default"\n')


def drop_plugin_tables(root):
    (root / "plugins.toml").write_text('default = "sr-v0"\n')


def drop_plugins_folder(root):
    shutil.rmtree(root / "plugins")


FAULTS = {
    "default plugin archived": (
        archive_sr_v0,
        "sr-v0: recorded as the default but its state is archived",
    ),
    "marketplace omits sr-v0": (omit_sr_v0, "sr-v0: state is default, the marketplace omits it"),
    "archived plugin listed, no folder": (
        list_archived_plugin_without_folder,
        "sr-old: state names no folder",
    ),
    "plugin name without prefix": (
        add_plugin_without_prefix,
        "old: plugin name does not start with 'sr-'",
    ),
    "offered plugin without description": (
        drop_description,
        "sr-v0: marketplace entry has no description",
    ),
    "name listed twice": (duplicate_sr_v0, "sr-v0: marketplace lists this name more than once"),
    "alias points at another folder": (
        point_alias_elsewhere,
        "simplicity-rules: marketplace source is",
    ),
    "alias without strict false": (drop_strict, "must set strict to false"),
    "evaluation states another state": (
        change_evaluation_state,
        "EVALUATION.md starts 'State: opt-in'",
    ),
    "empty evaluation": (empty_evaluation, "EVALUATION.md starts ''"),
    "marketplace is invalid JSON": (break_marketplace_json, "marketplace.json: cannot read"),
    "manifest is invalid JSON": (break_manifest_json, "plugin.json: cannot read"),
    "entry without a name": (add_unnamed_entry, "marketplace entry without a name"),
    "plugins.toml entry is not a table": (make_entry_not_a_table, "is not one of"),
    "plugins.toml has no plugin tables": (drop_plugin_tables, "default 'sr-v0' names no plugin"),
    "plugins folder missing": (drop_plugins_folder, "plugins: folder is missing"),
}


def run_check(root):
    return subprocess.run(
        [sys.executable, "-I", str(root / "scripts" / "check-plugins.py")],
        capture_output=True,
        text=True,
        check=False,
    )


class CheckPluginsTest(unittest.TestCase):
    def copy_catalog(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for name in CATALOG:
            source = REPO / name
            if source.is_dir():
                shutil.copytree(source, root / name)
            else:
                shutil.copy(source, root / name)
        return root

    def test_repository_passes(self):
        result = run_check(REPO)
        self.assertEqual((result.returncode, result.stdout), (0, "\n"))

    def test_faults_are_reported(self):
        for name, (apply_fault, expected) in FAULTS.items():
            with self.subTest(name):
                root = self.copy_catalog()
                apply_fault(root)
                result = run_check(root)
                self.assertEqual(result.returncode, 1)
                self.assertIn(expected, result.stdout)
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
