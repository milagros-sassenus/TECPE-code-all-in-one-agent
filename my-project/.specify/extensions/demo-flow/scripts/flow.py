"""Executable verification and guarded PR publishing for the Spec Kit demo."""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


class FlowError(RuntimeError):
    """A blocking workflow failure."""


def run(args: list[str], cwd: Path) -> str:
    if args[0] == "git":
        args = ["git", "--no-pager", *args[1:]]
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode:
        raise FlowError(
            f"Command failed ({result.returncode}): {args!r}\n"
            f"{result.stdout}\n{result.stderr}"
        )
    if result.stderr.strip() and "pip" in args and "list" in args:
        raise FlowError(f"Package index review was not clean:\n{result.stderr}")
    return result.stdout.strip()


def feature_directory(root: Path) -> Path:
    pointer = root / ".specify" / "feature.json"
    if not pointer.is_file():
        raise FlowError("No active feature. Run speckit-specify first.")
    feature = (
        root / json.loads(pointer.read_text(encoding="utf-8"))["feature_directory"]
    ).resolve()
    if not feature.is_relative_to(root.resolve()) or feature == root.resolve():
        raise FlowError("The active feature must be a directory within the project.")
    for name in ("spec.md", "plan.md", "tasks.md"):
        path = feature / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            raise FlowError(f"Missing or empty feature artifact: {path}")
    tasks = (feature / "tasks.md").read_text(encoding="utf-8")
    if re.search(r"^\s*[-*]\s+\[ \]", tasks, re.MULTILINE):
        raise FlowError("Feature tasks are incomplete; publication is blocked.")
    if not re.search(r"^\s*[-*]\s+\[[xX]\]", tasks, re.MULTILINE):
        raise FlowError("No completed feature tasks were found.")
    return feature


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def dependency_names(requirements: list[str]) -> set[str]:
    names = set()
    for requirement in requirements:
        match = re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", requirement)
        if not match:
            raise FlowError(f"Invalid dependency declaration: {requirement!r}")
        names.add(normalize(match.group()))
    return names


def verify(root: Path) -> dict:
    feature_directory(root)
    manifest = root / "pyproject.toml"
    if not manifest.is_file():
        raise FlowError(
            "pyproject.toml is missing; implement and install the API first."
        )
    python = (
        root
        / ".venv"
        / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    )
    if not python.is_file():
        raise FlowError(
            "Project .venv is missing. Create it and install declared tooling."
        )
    config = tomllib.loads(manifest.read_text(encoding="utf-8"))
    project = config.get("project", {})
    if "dependencies" in project.get("dynamic", []):
        raise FlowError("Declare runtime dependencies explicitly for this demo review.")
    direct = dependency_names(project.get("dependencies", []))
    for requirements in project.get("optional-dependencies", {}).values():
        direct.update(dependency_names(requirements))
    for requirements in config.get("dependency-groups", {}).values():
        direct.update(
            dependency_names([item for item in requirements if isinstance(item, str)])
        )
    outputs = {}
    for label, args in (
        ("tests", ["-m", "pytest"]),
        ("lint", ["-m", "ruff", "check", "."]),
        ("format", ["-m", "ruff", "format", "--check", "."]),
        ("dependencies", ["-m", "pip", "check"]),
    ):
        outputs[label] = run([str(python), *args], root)
    outdated = json.loads(
        run(
            [
                str(python),
                "-m",
                "pip",
                "list",
                "--outdated",
                "--format=json",
                "--disable-pip-version-check",
                "--retries",
                "0",
                "--timeout",
                "20",
            ],
            root,
        )
    )
    for package in outdated:
        package["dependency_type"] = (
            "direct" if normalize(package["name"]) in direct else "transitive/tooling"
        )
    return {"status": "passed", "checks": outputs, "outdated": outdated}


def publish(root: Path, title: str, body_file: str, files: list[str]) -> str:
    if not shutil.which("gh"):
        raise FlowError("GitHub CLI (gh) is missing. Install it and run gh auth login.")
    if not title.strip() or title.startswith("-"):
        raise FlowError("PR title must be nonempty and must not start with '-'.")
    feature = feature_directory(root)
    body = (root / body_file).resolve()
    if not body.is_relative_to(feature) or not body.is_file():
        raise FlowError(
            "PR body must be an existing file in the active feature directory."
        )
    repo_root = Path(run(["git", "rev-parse", "--show-toplevel"], root)).resolve()
    selected = []
    for name in files:
        path = (repo_root / name).resolve()
        if not path.is_relative_to(root.resolve()) or path.is_dir():
            raise FlowError(f"Select individual project files only: {name}")
        relative = path.relative_to(repo_root).as_posix()
        if not path.exists():
            run(
                [
                    "git",
                    "--literal-pathspecs",
                    "ls-files",
                    "--error-unmatch",
                    "--",
                    relative,
                ],
                repo_root,
            )
        selected.append(relative)
    if body.relative_to(repo_root).as_posix() not in selected:
        raise FlowError("Include the PR body document in --files.")
    staged = set(
        filter(
            None,
            run(["git", "diff", "--cached", "--name-only", "-z"], repo_root).split(
                "\0"
            ),
        )
    )
    if staged - set(selected):
        raise FlowError(
            "Unrelated staged changes exist. Preserve them and resolve before publishing."
        )
    changed = set(
        filter(None, run(["git", "diff", "--name-only", "-z"], repo_root).split("\0"))
    )
    if changed - set(selected):
        raise FlowError(
            "Unrelated tracked edits exist. Preserve them and resolve before publishing."
        )
    remote = run(["git", "remote", "get-url", "origin"], repo_root)
    match = re.fullmatch(
        r"(?:https://github\.com/|git@github\.com:)([\w.-]+/[\w.-]+?)(?:\.git)?",
        remote,
    )
    if not match:
        raise FlowError("origin must be an HTTPS or SSH github.com repository URL.")
    repository = match.group(1)
    run(["gh", "auth", "status", "--hostname", "github.com"], root)
    info = json.loads(
        run(
            [
                "gh",
                "repo",
                "view",
                repository,
                "--json",
                "defaultBranchRef",
            ],
            root,
        )
    )
    base = (info.get("defaultBranchRef") or {}).get("name")
    if not base:
        raise FlowError("Could not determine origin's default branch.")
    branch = run(["git", "branch", "--show-current"], repo_root)
    if not branch or branch in {base, "main", "master"}:
        raise FlowError(
            "Publication requires a feature branch, not the default branch or detached HEAD."
        )
    result = verify(root)
    print(json.dumps(result, indent=2))
    run(["git", "--literal-pathspecs", "add", "--", *selected], repo_root)
    changes = run(["git", "diff", "--cached", "--name-only"], repo_root)
    if changes:
        run(
            [
                "git",
                "commit",
                "-m",
                title,
                "-m",
                "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
            ],
            repo_root,
        )
    if run(["git", "status", "--porcelain", "--untracked-files=no"], repo_root):
        raise FlowError(
            "Uncommitted tracked changes remain. Resolve their scope before pushing."
        )
    run(["git", "push", "--set-upstream", "origin", branch], repo_root)
    existing = json.loads(
        run(
            [
                "gh",
                "pr",
                "list",
                "--repo",
                repository,
                "--head",
                branch,
                "--base",
                base,
                "--state",
                "open",
                "--json",
                "url",
            ],
            root,
        )
    )
    if len(existing) > 1:
        raise FlowError("Multiple matching open PRs found; resolve before continuing.")
    if existing:
        return existing[0]["url"]
    return run(
        [
            "gh",
            "pr",
            "create",
            "--repo",
            repository,
            "--head",
            branch,
            "--base",
            base,
            "--title",
            title,
            "--body-file",
            str(body),
        ],
        root,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root", type=Path, default=Path(__file__).resolve().parents[4]
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("verify")
    publication = commands.add_parser("publish")
    publication.add_argument("--title", required=True)
    publication.add_argument("--body-file", required=True)
    publication.add_argument("--files", nargs="+", required=True)
    args = parser.parse_args()
    try:
        root = args.project_root.resolve()
        if args.command == "verify":
            print(json.dumps(verify(root), indent=2))
        else:
            print(publish(root, args.title, args.body_file, args.files))
    except (FlowError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
