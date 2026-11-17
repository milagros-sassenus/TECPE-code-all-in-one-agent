# Demo hooks

The project registers two mandatory Spec Kit hooks in
[`extensions.yml`](../../extensions.yml):

1. `before_specify` invokes the bundled `speckit-git-feature` skill to create
   and switch to a numbered feature branch.
2. `after_implement` invokes `speckit-demo-flow-verify`. On success, that skill
   invokes `speckit-demo-flow-publish` to commit selected feature files, push
   the branch, and create or reuse an open GitHub PR.

There is no invented `after_verify` core event: publishing is an explicit
continuation of the custom verification command. The bundled workflow already
calls implement, so both full-flow and standalone implement runs reach the
same verification hook. Hooks run through the agent following the installed
skills, not as background filesystem watchers or CI jobs.

## Prerequisites

- Run from the application root, `my-project`.
- Use Git and a compatible Bash environment for the installed core skills.
  Git Bash may need its full Windows executable path if it is not on PATH.
- Commit or otherwise resolve existing demo setup changes before starting a
  feature. Do not mix unrelated edits or commits into a feature branch.
- The implemented API needs Python 3.11+, a project `.venv`,
  `pyproject.toml`, installed runtime dependencies, pytest, Ruff, and pip.
- Package review requires access to the configured package index. Outdated
  packages are advisory; failed or incomplete reviews block publication.
- Install GitHub CLI (`gh`), ensure it is on PATH, and authenticate using
  `gh auth login`. The account needs push and pull-request permissions.
  On Windows, reopen VS Code after installation to refresh its PATH.
  No tokens belong in project files.

## Usage

Ask Copilot to use `speckit-specify` for a new feature, then run plan, tasks,
analyze, and implement as usual. The mandatory hooks supply branch creation,
verification, dependency review, and PR publication. Review the spec and plan
before proceeding. The setup itself does not create an API or publish a PR.

To run only executable verification without publishing:

```text
python .specify/extensions/demo-flow/scripts/flow.py verify
```

For manual agent-driven verification and publication, invoke the
`speckit-demo-flow-verify` skill. A successful script run alone does not publish:
the skill also checks acceptance scenarios and selects the feature files.

Verification executes all pytest tests, Ruff lint and format checks, `pip check`,
and `pip list --outdated`. It requires completed feature tasks. Publication
repeats these checks, refuses default branches and unrelated staged/tracked
edits, stages only explicitly selected individual project files, includes the
Copilot coauthor trailer, and never force-pushes or merges.

## Test the automation without publishing

```text
python -m unittest discover -s .specify/extensions/demo-flow/tests -v
```

The tests use isolated temporary files and mock GitHub/network operations.
They do not commit, push, create a PR, or query the package index.
