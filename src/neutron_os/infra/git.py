"""Git helpers — subprocess wrappers for common git operations.

Provides a thin layer over ``git`` subprocess calls with consistent
error handling. No external dependencies (no GitPython, no pygit2).

Usage:
    from neutron_os.infra.git import run_git, git_sha, git_branch, git_is_dirty

    sha = git_sha(repo)               # current HEAD SHA
    branch = git_branch(repo)          # current branch name
    dirty = git_is_dirty(repo)         # uncommitted changes?
    output = run_git(repo, "log", "--oneline", "-5")  # arbitrary command
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(repo_root: Path, *args: str, check: bool = True) -> str:
    """Run a git command and return stdout.

    Args:
        repo_root: Working directory for the git command.
        *args: Arguments to ``git`` (e.g., ``"rev-parse"``, ``"HEAD"``).
        check: If True (default), raise on non-zero exit.

    Returns:
        Stripped stdout from the git command.

    Raises:
        subprocess.CalledProcessError: If check=True and git exits non-zero.
        FileNotFoundError: If git is not installed.
    """
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=check,
    )
    return result.stdout


def git_sha(repo_root: Path, *, short: bool = False) -> str:
    """Current HEAD commit SHA."""
    args = ["rev-parse"]
    if short:
        args.append("--short")
    args.append("HEAD")
    return run_git(repo_root, *args).strip()


def git_branch(repo_root: Path) -> str:
    """Current branch name (or 'HEAD' if detached)."""
    return run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD").strip()


def git_is_dirty(repo_root: Path) -> bool:
    """True if the working tree has uncommitted changes."""
    return bool(run_git(repo_root, "status", "--porcelain").strip())


def git_remote_url(repo_root: Path, remote: str = "origin") -> str | None:
    """Remote URL, or None if no remote configured."""
    try:
        return run_git(repo_root, "remote", "get-url", remote).strip()
    except subprocess.CalledProcessError:
        return None


def git_diff_files(
    repo_root: Path, since: str, path_filter: str = ""
) -> list[str]:
    """Files changed since a commit, optionally filtered by path prefix."""
    args = ["diff", "--name-only", since]
    if path_filter:
        args.extend(["--", path_filter])
    try:
        output = run_git(repo_root, *args)
        return [line.strip() for line in output.strip().splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []


__all__ = [
    "run_git",
    "git_sha",
    "git_branch",
    "git_is_dirty",
    "git_remote_url",
    "git_diff_files",
]
