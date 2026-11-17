---
description: "Publish the verified feature branch as a GitHub PR without staging unrelated changes."
---

# Publish the Feature

Run from the application root. This command requires GitHub CLI (`gh`) on PATH,
authenticated for the repository using `gh auth login`, and push/PR permission.
Never read or print tokens to work around missing authentication.

1. Read the active feature's spec, plan, tasks, and constitution.
   Independently confirm the implementation meets the acceptance scenarios.
   Stop if semantic verification is incomplete or there are known gaps.
2. Inspect Git status and relevant diffs. Identify exactly which files belong
   to this feature, including its specification documents. Exclude unrelated
   edits, secrets, `.env`, `.venv`, local databases, caches and temporary files.
   Do not use `git add .`, `git add -A`, amend, force-push, or discard edits.
   Review existing branch commits against the target base as well: they will
   all be published, not only the selected working-tree files. Stop if unrelated
   or sensitive content is already committed.
3. Write `pr-body.md` in the active feature directory with a feature summary,
   acceptance-scenario verification, test/lint results, dependency-review
   findings, and limitations. Include this document in the selected files.
4. Run the following, replacing placeholders with actual values:

   ```text
   python .specify/extensions/demo-flow/scripts/flow.py publish --title "feat: feature title" --body-file "specs/001-feature/pr-body.md" --files "my-project/specs/001-feature/spec.md" "my-project/specs/001-feature/plan.md" "my-project/specs/001-feature/tasks.md" "my-project/specs/001-feature/pr-body.md" "my-project/src/changed_file.py" "my-project/tests/test_changed_file.py"
   ```

   `--body-file` is relative to the application root. `--files` entries are
   individual file paths relative to the Git repository root, which may be
   the application's parent in a monorepo. Determine that root with
   `git rev-parse --show-toplevel`; do not assume the example prefix is correct.
   Include every feature file and pass each path separately.
5. The script reexecutes verification immediately before staging, commits only
   the selected files with a Copilot coauthor trailer, pushes the current
   feature branch without force, and creates a PR targeting origin's default
   branch. If that branch pair already has an open PR, it reuses its URL.
6. On any failure, stop and report the exact blocker. A successful push followed
   by a failed PR creation is NOT a successful publication; rerunning is safe.
   Never merge the PR automatically.
