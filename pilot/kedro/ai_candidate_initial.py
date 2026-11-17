#!/usr/bin/env python3
"""AI-produced first coding attempt for visible task kedro-org__kedro-4406.

Input was limited to the public problem statement and files at the pinned base commit.
No golden patch, hidden task test, future PR, or grader output informed the change.
This is the *first* attempt, not a post-pushback repair.
"""
from pathlib import Path
import argparse
import subprocess

BASE_COMMIT = "a565d6607d1d16933dbb1ea42cfb9de39ef80980"
ORIGINAL_BLOB_SHA1 = "0a0d0500982319bc24988078d33debecd85bda18"

ADDITION = '''

def load_ipython_extension(ipython) -> None:
    """Allow %load_ext kedro while keeping IPython imports lazy.

    The canonical internal entry point remains kedro.ipython.
    """
    from kedro.ipython import load_ipython_extension as _load_extension

    _load_extension(ipython)
'''

def apply(repo: Path) -> None:
    root = Path(repo).resolve()
    base = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    if base != BASE_COMMIT:
        raise ValueError(f"Source does not match frozen base commit: {base}")
    target = root / "kedro" / "__init__.py"
    actual_blob = subprocess.check_output(
        ["git", "-C", str(root), "hash-object", "kedro/__init__.py"], text=True
    ).strip()
    if actual_blob != ORIGINAL_BLOB_SHA1:
        raise ValueError("Original Kedro source blob mismatch")
    original = target.read_text(encoding="utf-8")
    if "def load_ipython_extension(" in original:
        raise ValueError("Existing extension entry point; refuse blind rewrite")
    if not original.endswith("\n"):
        raise ValueError("Unexpected source newline convention")
    target.write_text(original + ADDITION, encoding="utf-8")
    print("First attempt edited only kedro/__init__.py")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    apply(p.parse_args().repo)
