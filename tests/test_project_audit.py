from __future__ import annotations

import json
import importlib.util
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
CHECKER = ROOT / "scripts/check_toolkit.py"


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

    def test_plain_node_project(self):
        result = self.detect({"package.json": '{"name":"node-cli","bin":{"node-cli":"index.js"}}'})
        self.assertEqual(result["technologies"], ["nodejs"])

    def test_generated_and_dependency_directories_are_excluded(self):
        result = self.detect({
            "package.json": '{"name":"node-app"}',
            "node_modules/fake/package.json": '{"dependencies":{"@angular/core":"0.0.0"}}',
            "build/pubspec.yaml": "dependencies:\n  flutter:\n    sdk: flutter\n",
        })
        self.assertEqual(result["technologies"], ["nodejs"])
        self.assertEqual([item["path"] for item in result["manifests"]], ["package.json"])

    def test_invalid_package_json_does_not_execute_or_crash(self):
        result = self.detect({"package.json": "not-json"})
        self.assertEqual(result["technologies"], [])
        self.assertEqual(result["manifests"][0]["signals"], [])

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
    def run_installer(self, base: Path, mode: str = "--check", scope: str = "project", extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER), mode, "--scope", scope, "--target", str(base), "--resource", "project-audit", *(extra or [])],
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

    def test_user_preview_uses_personal_skill_location_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = self.run_installer(base, scope="user")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(base / ".agents/skills/project-audit"), result.stdout)
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

    def test_unknown_technology_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_installer(Path(directory), extra=["--technology", "typo"])
            self.assertEqual(result.returncode, 2)
            self.assertIn("unknown technologies", result.stderr)

    def test_invalid_source_manifest_is_an_error_in_dry_run(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            manifest = base / "manifest.json"
            data = json.loads((ROOT / "toolkit-manifest.json").read_text(encoding="utf-8"))
            data["resources"]["project-audit"]["source"] = "../outside"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_installer(base, mode="--dry-run", extra=["--manifest", str(manifest)])
            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid source path", result.stdout)
            self.assertFalse((base / ".agents").exists())


class ToolkitValidationTests(unittest.TestCase):
    def test_manifest_frontmatter_metadata_and_links(self):
        spec = importlib.util.spec_from_file_location("check_toolkit", CHECKER)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        errors: list[str] = []
        module.check_required(errors)
        module.check_manifest(errors)
        for path in module.files():
            module.check_content(path, errors)
            if path.name == "SKILL.md":
                module.check_skill(path, errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
