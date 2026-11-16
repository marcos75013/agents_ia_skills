from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts/install_toolkit.py"
MANIFEST = ROOT / "toolkit-manifest.json"
V2_AGENT = ROOT / "tests/fixtures/installer/v2/code-reviewer.toml"
STATE = Path(".codex/agents-ia-toolkit-state.json")


class SafeInstallerTests(unittest.TestCase):
    def run_installer(
        self,
        base: Path,
        mode: str,
        resources: tuple[str, ...] = ("project-audit", "code-reviewer"),
        manifest: Path = MANIFEST,
        scope: str = "project",
    ) -> subprocess.CompletedProcess[str]:
        resource_args = [argument for name in resources for argument in ("--resource", name)]
        return subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                mode,
                "--scope",
                scope,
                "--target",
                str(base),
                "--manifest",
                str(manifest),
                *resource_args,
            ],
            capture_output=True,
            text=True,
        )

    def v2_manifest(self, directory: Path) -> Path:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        data["toolkit_version"] = "0.5.0"
        agent = data["resources"]["code-reviewer"]
        agent["version"] = "0.2.0"
        agent["source"] = "tests/fixtures/installer/v2/code-reviewer.toml"
        path = directory / "manifest-v2.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_install_copies_both_resources_and_records_state(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = self.run_installer(base, "--install")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Applied successfully: 2 resource(s) changed", result.stdout)
            self.assertEqual(
                (base / ".codex/agents/code-reviewer.toml").read_bytes(),
                (ROOT / "agents/code-reviewer.toml").read_bytes(),
            )
            self.assertTrue((base / ".agents/skills/project-audit/SKILL.md").is_file())
            state = json.loads((base / STATE).read_text(encoding="utf-8"))
            self.assertEqual(state["toolkit_version"], "0.5.0")
            self.assertEqual(set(state["resources"]), {"project-audit", "code-reviewer"})

    def test_repeated_install_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            first = self.run_installer(base, "--install")
            before = (base / STATE).read_bytes()
            before_mtime = (base / STATE).stat().st_mtime_ns
            second = self.run_installer(base, "--install")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("Applied successfully: 0 resource(s) changed", second.stdout)
            self.assertEqual((base / STATE).read_bytes(), before)
            self.assertEqual((base / STATE).stat().st_mtime_ns, before_mtime)
            self.assertFalse((base / ".codex/toolkit-backups").exists())

    def test_preview_never_creates_state_or_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = self.run_installer(base, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((base / ".agents").exists())
            self.assertFalse((base / ".codex").exists())

    def test_install_mode_refuses_a_managed_update(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            self.assertEqual(self.run_installer(base, "--install", ("code-reviewer",)).returncode, 0)
            original = (base / ".codex/agents/code-reviewer.toml").read_bytes()
            v2 = self.v2_manifest(base)
            result = self.run_installer(base, "--install", ("code-reviewer",), v2)
            self.assertEqual(result.returncode, 1)
            self.assertIn("managed updates require --update", result.stderr)
            self.assertEqual((base / ".codex/agents/code-reviewer.toml").read_bytes(), original)

    def test_update_replaces_only_unmodified_managed_target_and_keeps_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            self.assertEqual(self.run_installer(base, "--install", ("code-reviewer",)).returncode, 0)
            original = (base / ".codex/agents/code-reviewer.toml").read_bytes()
            v2 = self.v2_manifest(base)
            preview = self.run_installer(base, "--check", ("code-reviewer",), v2)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertIn("UPDATE code-reviewer", preview.stdout)
            self.assertEqual((base / ".codex/agents/code-reviewer.toml").read_bytes(), original)
            result = self.run_installer(base, "--update", ("code-reviewer",), v2)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((base / ".codex/agents/code-reviewer.toml").read_bytes(), V2_AGENT.read_bytes())
            backups = list((base / ".codex/toolkit-backups/code-reviewer").glob("*/*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), original)
            state = json.loads((base / STATE).read_text(encoding="utf-8"))
            self.assertEqual(state["resources"]["code-reviewer"]["version"], "0.2.0")

    def test_update_refuses_locally_modified_target_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            self.assertEqual(self.run_installer(base, "--install", ("code-reviewer",)).returncode, 0)
            target = base / ".codex/agents/code-reviewer.toml"
            target.write_text("local customization\n", encoding="utf-8")
            state_before = (base / STATE).read_bytes()
            result = self.run_installer(base, "--update", ("code-reviewer",), self.v2_manifest(base))
            self.assertEqual(result.returncode, 1)
            self.assertIn("target was modified after installation", result.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), "local customization\n")
            self.assertEqual((base / STATE).read_bytes(), state_before)
            self.assertFalse((base / ".codex/toolkit-backups").exists())

    def test_conflict_aborts_the_whole_plan_before_any_write(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            conflict = base / ".agents/skills/project-audit"
            conflict.mkdir(parents=True)
            (conflict / "SKILL.md").write_text("local customization", encoding="utf-8")
            result = self.run_installer(base, "--install")
            self.assertEqual(result.returncode, 1)
            self.assertFalse((base / ".codex").exists())
            self.assertEqual((conflict / "SKILL.md").read_text(encoding="utf-8"), "local customization")

    def test_identical_unmanaged_target_can_be_adopted_without_copying(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            target = base / ".codex/agents/code-reviewer.toml"
            target.parent.mkdir(parents=True)
            shutil.copy2(ROOT / "agents/code-reviewer.toml", target)
            before = target.read_bytes()
            result = self.run_installer(base, "--install", ("code-reviewer",))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_bytes(), before)
            self.assertIn("code-reviewer", json.loads((base / STATE).read_text(encoding="utf-8"))["resources"])

    def test_symlinked_destination_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside_directory:
            base = Path(directory)
            outside = Path(outside_directory)
            (base / ".codex").symlink_to(outside, target_is_directory=True)
            result = self.run_installer(base, "--install", ("code-reviewer",))
            self.assertEqual(result.returncode, 2)
            self.assertIn("resolves outside the installation base", result.stderr)
            self.assertFalse((outside / "agents/code-reviewer.toml").exists())

    def test_user_scope_installs_to_personal_destinations(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = self.run_installer(base, "--install", scope="user")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((base / ".agents/skills/project-audit/SKILL.md").is_file())
            self.assertTrue((base / ".codex/agents/code-reviewer.toml").is_file())

    def test_invalid_state_aborts_before_target_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            state = base / STATE
            state.parent.mkdir(parents=True)
            state.write_text('{"schema_version": 1, "resources": {"code-reviewer": {"digest": "bad"}}}', encoding="utf-8")
            before = state.read_bytes()
            result = self.run_installer(base, "--install", ("code-reviewer",))
            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid installation state metadata", result.stderr)
            self.assertEqual(state.read_bytes(), before)
            self.assertFalse((base / ".codex/agents").exists())

    def test_state_write_failure_rolls_back_a_created_resource(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / ".codex").write_text("blocks the state directory\n", encoding="utf-8")
            result = self.run_installer(base, "--install", ("project-audit",))
            self.assertEqual(result.returncode, 2)
            self.assertIn("installation rolled back", result.stderr)
            self.assertFalse((base / ".agents/skills/project-audit").exists())
            self.assertEqual((base / ".codex").read_text(encoding="utf-8"), "blocks the state directory\n")


if __name__ == "__main__":
    unittest.main()
