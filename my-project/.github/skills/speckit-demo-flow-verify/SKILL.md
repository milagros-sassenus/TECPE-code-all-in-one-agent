---
name: speckit-demo-flow-verify
description: Verify the Python feature and review outdated packages before publishing
  its pull request.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: extension:demo-flow
---

# Demo Flow Verify Skill

# Verify the Feature

Run from the application root (the directory containing `.specify`).

1. Read the active feature from `.specify/feature.json`, its spec, plan, tasks,
   and the constitution. Confirm the implementation matches the acceptance
   scenarios, not only that tests pass. If there are gaps, stop and report them.
2. Run `python .specify/extensions/demo-flow/scripts/flow.py verify`.
   The script uses the project's `.venv` interpreter, not global packages.
   Missing tasks, an incomplete task, tests failing or collecting no tests,
   lint/formatting errors, broken installed dependencies, and an unavailable
   package index are blocking failures.
3. If any step fails, STOP. Do not commit, push, publish, or report success.
   Fix only issues within the feature's scope, and rerun verification.
4. Compare the dependency results with `pyproject.toml` and the lockfile when
   present; explain any differences. Report outdated packages as a table: package, installed version, latest
   version, direct/transitive type, and recommendation. A newer version alone
   is advisory, not a blocking failure. Consult official release notes and
   Python compatibility before recommending an upgrade. Never upgrade
   automatically or equate outdated with vulnerable.
5. Only when the implementation and all checks pass, invoke the
   `speckit-demo-flow-publish` skill and wait for its result. Do not merely
   mention its name. The user has requested automatic PR creation for
   completed features; do not require another confirmation for that normal
   path. Stop and ask if unrelated changes cannot be safely separated.
6. Report the PR URL, or explicitly report the publication blocker. Never
   claim the full flow is complete if verification or publication failed.
