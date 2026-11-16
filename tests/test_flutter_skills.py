from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts/install_toolkit.py"
MANIFEST = ROOT / "toolkit-manifest.json"
ARCHITECTURE = ROOT / "skills/flutter-clean-architecture/SKILL.md"
CUBIT = ROOT / "skills/flutter-cubit/SKILL.md"


class FlutterSkillContractTests(unittest.TestCase):
    def test_skills_have_distinct_scope_and_migration_boundaries(self):
        architecture = ARCHITECTURE.read_text(encoding="utf-8")
        cubit = CUBIT.read_text(encoding="utf-8")
        self.assertIn("feature-first", architecture)
        self.assertIn("domain` to Flutter", architecture)
        self.assertIn("repository-wide migration", architecture)
        self.assertIn("installed `flutter_bloc` version", cubit)
        self.assertIn("stale asynchronous results", cubit)
        self.assertIn("another state-management approach", cubit)
        self.assertNotEqual(architecture, cubit)

    def test_manifest_exposes_both_flutter_only_skills(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["toolkit_version"], "0.5.0")
        for name in ("flutter-clean-architecture", "flutter-cubit"):
            resource = manifest["resources"][name]
            self.assertEqual(resource["kind"], "skill")
            self.assertEqual(resource["technologies"], ["flutter"])
            self.assertEqual(resource["source"], f"skills/{name}")
            self.assertEqual(resource["destinations"]["project"], f".agents/skills/{name}")


class FlutterProfileInstallerTests(unittest.TestCase):
    def run_installer(self, base: Path, technology: str, mode: str = "--check") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                mode,
                "--scope",
                "project",
                "--target",
                str(base),
                "--technology",
                technology,
            ],
            capture_output=True,
            text=True,
        )

    def test_flutter_profile_selects_common_and_flutter_resources_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = self.run_installer(base, "flutter")
            self.assertEqual(result.returncode, 0, result.stderr)
            for name in ("project-audit", "code-reviewer", "flutter-clean-architecture", "flutter-cubit"):
                self.assertIn(f"CREATE {name}", result.stdout)
            self.assertFalse((base / ".agents").exists())
            self.assertFalse((base / ".codex").exists())

    def test_angular_profile_skips_flutter_specific_resources(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_installer(Path(directory), "angular")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("CREATE project-audit", result.stdout)
            self.assertIn("CREATE code-reviewer", result.stdout)
            self.assertIn("SKIP flutter-clean-architecture", result.stdout)
            self.assertIn("SKIP flutter-cubit", result.stdout)

    def test_flutter_profile_installs_all_selected_resources_and_state(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = self.run_installer(base, "flutter", "--install")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((base / ".agents/skills/project-audit/SKILL.md").is_file())
            self.assertTrue((base / ".agents/skills/flutter-clean-architecture/SKILL.md").is_file())
            self.assertTrue((base / ".agents/skills/flutter-cubit/SKILL.md").is_file())
            self.assertTrue((base / ".codex/agents/code-reviewer.toml").is_file())
            state = json.loads((base / ".codex/agents-ia-toolkit-state.json").read_text(encoding="utf-8"))
            self.assertEqual(
                set(state["resources"]),
                {"project-audit", "code-reviewer", "flutter-clean-architecture", "flutter-cubit"},
            )


if __name__ == "__main__":
    unittest.main()
