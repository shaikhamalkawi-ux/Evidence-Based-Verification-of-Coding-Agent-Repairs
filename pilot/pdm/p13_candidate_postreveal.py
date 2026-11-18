#!/usr/bin/env python3
"""P13 POST-REVEAL diagnostic: retain PDM Requirement identity while expanding groups.

This code was developed AFTER P12's original hidden oracle was revealed.
It is exploratory and must NEVER be counted as a new blinded agent repair,
a real developer-follow-up case, or a prospective X1 policy result.

The repair hypothesis was developed from public PDM source and two failures in
the pre-existing public test_update.py tests. No benchmark test patch is read.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

BASE_SHA = "564d09acbf2c8ef6500a3864f1fa1d38b3c5cdd5"
SOURCE_BLOB_SHA = "02c49f0a135429508c2eca400a63d1a9f7b9e335"
TARGET = "src/pdm/cli/commands/update.py"
ORIGINAL = "        reqs = [r for g, deps in all_dependencies.items() for r in deps if locked_groups is None or g in locked_groups]"
REPLACEMENT = """        # Retain the selected direct Requirement objects: earlier in do_update,
        # --unconstrained and --prerelease have already modified their attributes.
        # A fresh get_dependencies() call alone discards those modifications.
        reqs = []
        for group, direct_deps in all_dependencies.items():
            if locked_groups is not None and group not in locked_groups:
                continue
            direct_by_identity = {r.identify(): r for r in direct_deps}
            for expanded in project.get_dependencies(group):
                original = direct_by_identity.get(expanded.identify())
                if original is None:
                    reqs.append(expanded)
                else:
                    # Combine provenance while keeping prerelease/specifier edits.
                    original.groups = sorted(set(original.groups) | set(expanded.groups))
                    reqs.append(original)
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def main(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != BASE_SHA:
        raise ValueError("Incorrect upstream base. Refusing diagnostic changes.")
    if git(repo, "hash-object", TARGET) != SOURCE_BLOB_SHA:
        raise ValueError("Upstream source differs from pinned PDM file.")
    f = repo / TARGET
    old = f.read_text(encoding="utf-8")
    if old.count(ORIGINAL) != 1:
        raise ValueError("Expected source statement is missing or duplicated.")
    f.write_text(old.replace(ORIGINAL, REPLACEMENT), encoding="utf-8")
    subprocess.run(["python3", "-m", "py_compile", str(f)], check=True)
    subprocess.run(["git", "-C", str(repo), "diff", "--check"], check=True)
    changed = git(repo, "diff", "--name-only").splitlines()
    if changed != [TARGET]:
        raise ValueError(f"Unexpected modifications: {changed}")
    print("P13_PUBLIC_MECHANISM_PATCH_ONLY=" + TARGET)
    print("P13_POSTREVEAL_UNBLINDED_NO_FEEDBACK_INFERENCE")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True, type=Path)
    main(p.parse_args().repo.resolve())
