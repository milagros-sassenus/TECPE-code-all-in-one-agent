# Mili Project Demo Instructions

## Project Scope

This is a fictional, local-only Spec Kit demo. The application has not been
implemented yet. Do not treat planned packages, commands, or features as
already available.

## Source of Truth

Read the [project constitution](../.specify/memory/constitution.md) before
planning or implementing a feature. It defines the authoritative stack,
quality gates, and demo constraints; do not duplicate or silently override it.

The backend API MUST use Python and FastAPI, not Node.js or TypeScript.
Keep changes limited to the requested feature and use fictional example data.
Respond to the user in Spanish.

## Simplicity First

Always prefer the simplest solution that fully satisfies the requirements.
Avoid unnecessary abstractions, dependencies, configuration, and files.
Reuse existing patterns and tools before introducing new ones. Do not build
for hypothetical future needs. Simplicity must not compromise correctness,
security, or required validation.

## Spec Kit Workflow

- Use the installed `speckit-*` skills when the user requests that workflow.
- Treat `my-project` as the application root; execute project commands there.
- Read the active feature's specification, plan, and tasks before coding.
  Resolve its directory through `.specify/feature.json` when it exists;
  do not infer it from the Git branch name.
- Keep generic Spec Kit templates and installed skill definitions intact.
  Put feature-specific decisions in the feature artifacts.
- When asked only to prepare rules or documentation, do not implement the API,
  install dependencies, or generate an unsolicited feature.
- The installed Spec Kit scripts use Bash. On Windows, run those scripts
  through a compatible Bash environment, not directly as PowerShell scripts.
- Before creating a feature branch, stop if the working tree has unrelated
  uncommitted changes. Do not silently include demo setup changes in a feature.
- Honor the mandatory hooks in [extensions.yml](../.specify/extensions.yml).
  `before_specify` creates a feature branch; `after_implement` invokes
  `speckit-demo-flow-verify`, which publishes a PR only after verification.
  Do not skip hooks when running the full workflow or invoke them twice.

## Validation

During implementation, declare the required tooling before running the
constitution's checks. Report actual results and blockers, not assumed
success. Documentation-only changes do not require application tests.
Follow the constitution's dependency review before dependency changes and
feature completion. Report outdated packages and recommendations without
automatically upgrading them; distinguish newer releases from end of support
or known vulnerabilities.

## Feature Publication

Follow the [demo hook workflow](../.specify/extensions/demo-flow/README.md).
The verification skill checks acceptance scenarios, runs the executable
checks, and invokes `speckit-demo-flow-publish` only on success. Never open a PR
after a failed or skipped required check. The publishing script repeats
verification before committing, pushing, and creating or reusing the PR.
Do not include unrelated edits or commits, publish secrets, force-push, or
merge automatically. Missing tooling or GitHub authentication is a blocker,
not a reason to bypass checks. Preparing this automation does not authorize
publishing the current demo setup changes.
