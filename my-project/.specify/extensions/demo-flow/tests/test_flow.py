import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import flow


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name).resolve()
        self.root = self.repo / "my-project"
        self.feature = self.root / "specs" / "001-demo"
        self.feature.mkdir(parents=True)
        (self.root / ".specify").mkdir()
        (self.root / ".specify" / "feature.json").write_text(
            json.dumps({"feature_directory": "specs/001-demo"}), encoding="utf-8"
        )
        for name in ("spec.md", "plan.md", "pr-body.md"):
            (self.feature / name).write_text("Demo feature", encoding="utf-8")
        (self.feature / "tasks.md").write_text(
            "- [X] T001 Demo task\n", encoding="utf-8"
        )
        (self.root / "pyproject.toml").write_text(
            '[project]\nname = "demo"\nversion = "0.1.0"\n'
            'dependencies = ["FastAPI>=0.100"]\n',
            encoding="utf-8",
        )
        executable = (
            self.root
            / ".venv"
            / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        )
        executable.parent.mkdir(parents=True)
        executable.touch()
        self.files = ["my-project/specs/001-demo/pr-body.md"]
        self.commands = []
        self.existing = []
        self.branch = "001-demo"
        self.staged = ""
        self.changed = ""

    def command(self, args, cwd):
        self.commands.append(args)
        if args[:2] == ["git", "rev-parse"]:
            return str(self.repo)
        if args[:3] == ["git", "remote", "get-url"]:
            return "https://github.com/example/demo.git"
        if args[:3] == ["gh", "repo", "view"]:
            return '{"defaultBranchRef": {"name": "main"}}'
        if args[:3] == ["git", "branch", "--show-current"]:
            return self.branch
        if args[:4] == ["git", "diff", "--cached", "--name-only"]:
            return (
                self.staged if "-z" in args else "my-project/specs/001-demo/pr-body.md"
            )
        if args[:3] == ["git", "diff", "--name-only"]:
            return self.changed
        if args[:3] == ["gh", "pr", "list"]:
            return json.dumps(self.existing)
        if args[:3] == ["gh", "pr", "create"]:
            return "https://github.com/example/demo/pull/1"
        if "--outdated" in args:
            return '[{"name":"fastapi","version":"0.100","latest_version":"0.120"}]'
        return ""

    def publish(self):
        with (
            patch.object(flow.shutil, "which", return_value="gh"),
            patch.object(flow, "run", side_effect=self.command),
            patch.object(flow, "verify", return_value={"status": "passed"}),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            return flow.publish(
                self.root, "feat: demo", "specs/001-demo/pr-body.md", self.files
            )

    def test_outdated_packages_are_advisory_and_classified(self):
        with patch.object(flow, "run", side_effect=self.command):
            result = flow.verify(self.root)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["outdated"][0]["dependency_type"], "direct")
        self.assertEqual(len(result["checks"]), 4)
        self.assertTrue(
            all(str(self.root / ".venv") in args[0] for args in self.commands)
        )

    def test_incomplete_tasks_block_checks(self):
        (self.feature / "tasks.md").write_text("- [ ] T001 Pending", encoding="utf-8")
        with (
            patch.object(flow, "run") as run,
            self.assertRaisesRegex(flow.FlowError, "incomplete"),
        ):
            flow.verify(self.root)
        run.assert_not_called()

    def test_missing_environment_blocks_checks(self):
        executable = next((self.root / ".venv").rglob("*python*"))
        executable.unlink()
        with self.assertRaisesRegex(flow.FlowError, ".venv is missing"):
            flow.verify(self.root)

    def test_failed_tests_stop_lint_and_review(self):
        with (
            patch.object(
                flow, "run", side_effect=flow.FlowError("no tests collected")
            ) as run,
            self.assertRaisesRegex(flow.FlowError, "no tests"),
        ):
            flow.verify(self.root)
        self.assertEqual(run.call_count, 1)

    def test_pip_index_warning_with_zero_exit_is_blocking(self):
        result = subprocess.CompletedProcess([], 0, "[]", "WARNING: connection failed")
        with (
            patch.object(flow.subprocess, "run", return_value=result),
            self.assertRaisesRegex(flow.FlowError, "not clean"),
        ):
            flow.run(["python", "-m", "pip", "list", "--outdated"], self.root)

    def test_nonzero_command_exit_is_blocking(self):
        result = subprocess.CompletedProcess([], 5, "no tests ran", "")
        with (
            patch.object(flow.subprocess, "run", return_value=result),
            self.assertRaisesRegex(flow.FlowError, "Command failed"),
        ):
            flow.run(["python", "-m", "pytest"], self.root)

    def test_missing_gh_blocks_publication(self):
        with (
            patch.object(flow.shutil, "which", return_value=None),
            self.assertRaisesRegex(flow.FlowError, "GitHub CLI"),
        ):
            flow.publish(
                self.root, "feat: demo", "specs/001-demo/pr-body.md", self.files
            )

    def test_feature_path_cannot_escape_project(self):
        (self.root / ".specify" / "feature.json").write_text(
            '{"feature_directory": ".."}', encoding="utf-8"
        )
        with self.assertRaisesRegex(flow.FlowError, "within the project"):
            flow.feature_directory(self.root)

    def test_main_branch_never_publishes(self):
        self.branch = "main"
        with self.assertRaisesRegex(flow.FlowError, "feature branch"):
            self.publish()
        self.assertFalse(any("push" in args for args in self.commands))

    def test_unrelated_staged_changes_never_commit(self):
        self.staged = "unrelated.txt\0"
        with self.assertRaisesRegex(flow.FlowError, "Unrelated staged"):
            self.publish()
        self.assertFalse(any("commit" in args for args in self.commands))

    def test_unrelated_tracked_changes_never_commit(self):
        self.changed = "unrelated.txt\0"
        with self.assertRaisesRegex(flow.FlowError, "Unrelated tracked"):
            self.publish()
        self.assertFalse(any("commit" in args for args in self.commands))

    def test_verification_failure_never_stages_or_pushes(self):
        with (
            patch.object(flow.shutil, "which", return_value="gh"),
            patch.object(flow, "run", side_effect=self.command),
            patch.object(flow, "verify", side_effect=flow.FlowError("tests failed")),
            self.assertRaisesRegex(flow.FlowError, "tests failed"),
        ):
            flow.publish(
                self.root, "feat: demo", "specs/001-demo/pr-body.md", self.files
            )
        self.assertFalse(any("add" in args or "push" in args for args in self.commands))

    def test_success_commits_pushes_and_creates_pr_in_order(self):
        self.assertEqual(self.publish(), "https://github.com/example/demo/pull/1")
        commit = next(args for args in self.commands if "commit" in args)
        self.assertIn("Co-authored-by: Copilot", commit[-1])
        commit_index = self.commands.index(commit)
        push_index = next(i for i, args in enumerate(self.commands) if "push" in args)
        create_index = next(
            i
            for i, args in enumerate(self.commands)
            if args[:3] == ["gh", "pr", "create"]
        )
        self.assertLess(commit_index, push_index)
        self.assertLess(push_index, create_index)
        stage = next(args for args in self.commands if "add" in args)
        self.assertEqual(
            stage, ["git", "--literal-pathspecs", "add", "--", *self.files]
        )

    def test_existing_pr_is_reused(self):
        self.existing = [{"url": "https://github.com/example/demo/pull/2"}]
        self.assertEqual(self.publish(), self.existing[0]["url"])
        self.assertFalse(
            any(args[:3] == ["gh", "pr", "create"] for args in self.commands)
        )

    def test_push_failure_never_creates_pr(self):
        command = self.command

        def fail_push(args, cwd):
            if "push" in args:
                raise flow.FlowError("push rejected")
            return command(args, cwd)

        with (
            patch.object(flow.shutil, "which", return_value="gh"),
            patch.object(flow, "run", side_effect=fail_push),
            patch.object(flow, "verify", return_value={"status": "passed"}),
            contextlib.redirect_stdout(io.StringIO()),
            self.assertRaisesRegex(flow.FlowError, "push rejected"),
        ):
            flow.publish(
                self.root, "feat: demo", "specs/001-demo/pr-body.md", self.files
            )
        self.assertFalse(
            any(args[:3] == ["gh", "pr", "create"] for args in self.commands)
        )


if __name__ == "__main__":
    unittest.main()
