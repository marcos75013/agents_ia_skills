from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DETECTOR = ROOT / "skills/project-audit/scripts/detect_project.py"
INSTALLER = ROOT / "scripts/install_toolkit.py"
SKILL = ROOT / "skills/project-audit/SKILL.md"


class ProjectAuditDetectionTests(unittest.TestCase):
    def detect(self, files: dict[str, str]) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(DETECTOR), str(root)],
                check=True,
                capture_output=True,
                text=True,
            )
            return json.loads(result.stdout)

    def test_flutter(self):
        result = self.detect({"pubspec.yaml": "dependencies:\n  flutter:\n    sdk: flutter\n"})
        self.assertEqual(result["technologies"], ["flutter"])

    def test_angular_is_not_misclassified_as_node_backend(self):
        result = self.detect({
            "angular.json": "{}",
            "package.json": '{"dependencies":{"@angular/core":"^20.0.0"}}',
        })
        self.assertEqual(result["technologies"], ["angular"])

    def test_spring_boot(self):
        result = self.detect({"pom.xml": "<parent><artifactId>spring-boot-starter-parent</artifactId></parent>"})
        self.assertEqual(result["technologies"], ["spring-boot"])

    def test_node_backend(self):
        result = self.detect({"package.json": '{"dependencies":{"express":"^5.0.0"}}'})
        self.assertEqual(result["technologies"], ["nodejs"])

    def test_multi_technology(self):
        result = self.detect({
            "mobile/pubspec.yaml": "dependencies:\n  flutter:\n    sdk: flutter\n",
            "web/angular.json": "{}",
            "web/package.json": '{"dependencies":{"@angular/core":"^20.0.0"}}',
            "api/pom.xml": "<artifactId>spring-boot-starter-web</artifactId>",
            "worker/package.json": '{"dependencies":{"fastify":"^5.0.0"}}',
        })
        self.assertEqual(result["technologies"], ["angular", "flutter", "nodejs", "spring-boot"])

    def test_skill_routes_all_supported_profiles_and_is_read_only(self):
        instructions = SKILL.read_text(encoding="utf-8")
        for reference in ("flutter.md", "angular.md", "spring-boot.md", "nodejs.md"):
            self.assertIn(f"references/{reference}", instructions)
        self.assertIn("Do not edit files", instructions)
        self.assertIn("facts, findings, recommendations and unverified items separately", instructions)


class InstallerPreviewTests(unittest.TestCase):
    def run_installer(self, base: Path, mode: str = "--check") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER), mode, "--scope", "project", "--target", str(base), "--resource", "project-audit"],
            capture_output=True,
            text=True,
        )

    def test_preview_reports_create_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = self.run_installer(base)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("CREATE project-audit", result.stdout)
            self.assertFalse((base / ".agents").exists())

    def test_check_detects_conflict(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            target = base / ".agents/skills/project-audit"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("local customization", encoding="utf-8")
            result = self.run_installer(base)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CONFLICT project-audit", result.stdout)

    def test_check_recognizes_identical_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            target = base / ".agents/skills/project-audit"
            shutil.copytree(ROOT / "skills/project-audit", target)
            result = self.run_installer(base)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("UNCHANGED project-audit", result.stdout)


if __name__ == "__main__":
    unittest.main()
