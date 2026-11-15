from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "agents/code-reviewer.toml"
CASES = ROOT / "tests/fixtures/code-review/cases.json"
INSTALLER = ROOT / "scripts/install_toolkit.py"


class CodeReviewerConfigurationTests(unittest.TestCase):
    def test_agent_uses_current_codex_schema_and_read_only_contract(self):
        data = tomllib.loads(AGENT.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "code_reviewer")
        self.assertTrue(data["description"])
        instructions = data["developer_instructions"]
        for phrase in (
            "Stay read-only",
            "Start with the diff",
            "Do not scan the whole repository",
            "Do not invent findings",
            "If there is no justified finding",
            "severity",
            "file and diff line",
            "probable impact",
            "concrete recommendation",
            "confidence",
            "Clean Architecture feature-first",
        ):
            self.assertIn(phrase, instructions)
        for forbidden in ("sandbox_mode", "approval_policy", "model_provider", "mcp_servers"):
            self.assertNotIn(forbidden, data)
        self.assertIs(data["features"]["request_permissions_tool"], False)

    def test_evaluation_cases_cover_technologies_findings_and_clean_diffs(self):
        fixture = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(fixture["schema_version"], 1)
        cases = fixture["cases"]
        self.assertEqual(
            {case["technology"] for case in cases},
            {"flutter", "angular", "spring-boot", "nodejs"},
        )
        findings = [case for case in cases if case["classification"] == "known-finding"]
        clean = [case for case in cases if case["classification"] == "clean"]
        self.assertGreaterEqual(len(findings), 4)
        self.assertGreaterEqual(len(clean), 2)
        for case in cases:
            self.assertTrue(case["id"])
            self.assertIn("diff --git", case["diff"])
        for case in findings:
            self.assertIn(case["expected_severity"], {"critical", "high", "medium", "low"})
            self.assertIn(case["expected_file"], case["diff"])


class CodeReviewerInstallerPreviewTests(unittest.TestCase):
    def run_installer(self, base: Path, scope: str = "project") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                "--check",
                "--scope",
                scope,
                "--target",
                str(base),
                "--resource",
                "code-reviewer",
            ],
            capture_output=True,
            text=True,
        )

    def test_project_preview_targets_codex_agent_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = self.run_installer(base)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("CREATE code-reviewer", result.stdout)
            self.assertIn(str(base / ".codex/agents/code-reviewer.toml"), result.stdout)
            self.assertFalse((base / ".codex").exists())

    def test_user_preview_targets_codex_agent_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result = self.run_installer(base, scope="user")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(base / ".codex/agents/code-reviewer.toml"), result.stdout)
            self.assertFalse((base / ".codex").exists())

    def test_agent_conflict_is_detected_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            target = base / ".codex/agents/code-reviewer.toml"
            target.parent.mkdir(parents=True)
            target.write_text('name = "local_reviewer"\n', encoding="utf-8")
            result = self.run_installer(base)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CONFLICT code-reviewer", result.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), 'name = "local_reviewer"\n')

    def test_identical_agent_is_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            target = base / ".codex/agents/code-reviewer.toml"
            target.parent.mkdir(parents=True)
            shutil.copyfile(AGENT, target)
            result = self.run_installer(base)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("UNCHANGED code-reviewer", result.stdout)


if __name__ == "__main__":
    unittest.main()
