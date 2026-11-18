#!/usr/bin/env python3
"""P12 first, visible-only GPT-6 research candidate for original PDM task.

No benchmark oracle or gold patch is read. Only changes the locked historical
src/pdm/cli/commands/update.py file (one source statement). The synthetic Git
author label in a later CI commit is NOT independently attested agent authorship.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

BASE_SHA = "564d09acbf2c8ef6500a3864f1fa1d38b3c5cdd5"
SOURCE_BLOB_SHA = "02c49f0a135429508c2eca400a63d1a9f7b9e335"
TARGET = "src/pdm/cli/commands/update.py"
OLD = "        reqs = [r for g, deps in all_dependencies.items() for r in deps if locked_groups is None or g in locked_groups]"
NEW = """        reqs = [
            req
            for group in all_dependencies
            if locked_groups is None or group in locked_groups
            for req in project.get_dependencies(group)
        ]"""


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def main(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != BASE_SHA:
        raise ValueError("Wrong upstream base SHA; refuse edits")
    if git(repo, "hash-object", TARGET) != SOURCE_BLOB_SHA:
        raise ValueError("Upstream file changed; refuse edits")
    target = repo / TARGET
    original = target.read_text(encoding="utf-8")
    if original.count(OLD) != 1:
        raise ValueError("Expected exactly one original update requirement-collection statement")
    modified = original.replace(OLD, NEW)
    target.write_text(modified, encoding="utf-8")
    subprocess.run(["python3", "-m", "py_compile", str(target)], check=True)
    subprocess.run(["git", "-C", str(repo), "diff", "--check"], check=True)
    changed = git(repo, "diff", "--name-only").splitlines()
    if changed != [TARGET]:
        raise ValueError(f"Unexpected source changes: {changed}")
    print("P12_FIRST_CANDIDATE_CHANGED_ONLY=" + TARGET)
    print("P12_FIRST_CANDIDATE_MODE=AI_GENERATED_VISIBLE_ONLY_NOT_AUTHENTICATED_AGENT")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    main(ap.parse_args().repo.resolve())
