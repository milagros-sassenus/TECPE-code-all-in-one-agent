# Mili Project Constitution

This is a fictional, local-only project for demonstrating Spec Kit.
These sample rules are demo defaults, not production-readiness guarantees.

## Core Principles

### I. Specify Before Implementing

Every feature MUST define its users, scope, acceptance scenarios, edge cases,
and measurable success criteria before implementation. Requirements describe
observable behavior; implementation choices belong in the plan. Unresolved
decisions that change behavior MUST be clarified with the user.

### II. Python API First

The backend API MUST use Python 3.11 or newer, FastAPI, and Pydantic for request
and response validation. HTTP endpoints MUST use JSON under `/api/v1`.
Use SQLite when persistence is required. Do not introduce another backend
language, framework, or database without an approved constitution amendment.

### III. Small, Understandable Solutions

Use a single application with thin routes and separate business logic when
needed. Add abstractions only for demonstrated requirements. Microservices,
message brokers, cloud infrastructure, and a frontend are out of scope unless
explicitly requested. New dependencies MUST have a documented purpose.

### IV. Observable, Testable Behavior

Every acceptance scenario MUST map to a task and an automated pytest test.
Changed endpoints MUST cover successful requests, invalid input, and missing
resources where applicable. Use FastAPI TestClient for API integration tests.
Defect fixes MUST include a regression test. Tests MUST be isolated and use
temporary storage rather than shared or real user data.

### V. Explicit Errors and Safe Demo Data

Never hide exceptions or return successful responses when an operation fails.
Use appropriate HTTP status codes and actionable error messages. Log unexpected
failures without exposing stack traces to API consumers. Use fictional data
only; never commit secrets, credentials, local databases, or personal data.

## Technical and Demo Constraints

- The API MUST run locally without paid services or external credentials.
- Use a project-local `.venv` and declare dependencies in `pyproject.toml`.
- Python identifiers and API fields use English; explanations to the user use
  Spanish. Public functions MUST have type annotations.
- Use Ruff for formatting and linting, and pytest for automated tests.
- Use conventional HTTP statuses: 201 for creation, 404 for missing resources,
  and FastAPI's 422 validation responses for invalid request data.
- Paginated list endpoints MUST default to 20 items and cap page size at 100.
- Local demo runs MUST bind to loopback by default. Authentication and public
  deployment are not part of the baseline; never present it as production-ready.
- Each implemented feature MUST document local startup, required configuration,
  and at least one reproducible usage example.

## Dependency Review

- Before adding or changing dependencies, and before declaring a feature
  complete, review the installed packages in the project's `.venv` with
  `python -m pip list --outdated --format=json`. Confirm that `python` resolves
  to that environment before running the command.
- Compare results with `pyproject.toml` and the lockfile, when present.
  Distinguish direct dependencies from transitive dependencies.
- Report each outdated package's installed version, latest available version,
  dependency type, and recommended action. Check official release notes and
  Python compatibility before recommending an upgrade.
- A newer release does not mean the installed package is expired, unsupported,
  or vulnerable. Only claim end of support or a vulnerability when supported
  by an official lifecycle notice or security advisory.
- Do not automatically upgrade packages or introduce breaking changes.
  Obtain approval before changing versions, and run affected tests afterward.
- If the environment is missing, packages are not installed, or the package
  index cannot be reached, report the review as blocked or not run with the
  reason. Do not report that dependencies are current without a successful
  check. Documentation-only changes do not require a dependency review.

## Development Workflow and Quality Gates

1. Use `speckit-specify` for one feature, then review its scope and acceptance
   scenarios. Use `speckit-clarify` when important ambiguity remains.
2. Use `speckit-plan` to define the design and explicitly check compliance with
   all five principles and the technical constraints above.
3. Use `speckit-tasks` to produce actionable tasks, including tests and related
   documentation. Use `speckit-analyze` before implementation.
4. Resolve critical inconsistencies before running `speckit-implement`.
5. Before declaring completion, run the relevant pytest tests,
   `python -m ruff check .`, and `python -m ruff format --check .` from the
   project directory. Tooling MUST be declared during implementation before
   these commands are expected to work.
6. Report the commands executed, their results, and remaining blockers. Never
   claim a check passed if it was not run. Use `speckit-converge` when checking
   whether an implementation still has gaps against its approved artifacts.

## Governance

This constitution is the source of truth for project rules. Feature specs,
plans, tasks, and agent instructions MUST remain consistent with it.
If a requested change conflicts with a rule, explain the conflict and obtain
approval before changing the rule or implementing the conflicting behavior.

Amendments MUST document their reason and update the version and amendment
date. Use a major version for incompatible rule changes, a minor version for
new rules, and a patch version for clarifications. Recheck affected feature
artifacts after an amendment. The initial version replaces the empty template;
it does not assert that any application code or tooling already exists.

### Amendment History

- 1.0.0: Replace the empty template with fictional demo rules and a Python API
  stack.
- 1.1.0: Add dependency freshness reviews at the user's request to make package
  maintenance visible during the demo.

**Version**: 1.1.0 | **Ratified**: 2026-11-17 | **Last Amended**: 2026-11-17
