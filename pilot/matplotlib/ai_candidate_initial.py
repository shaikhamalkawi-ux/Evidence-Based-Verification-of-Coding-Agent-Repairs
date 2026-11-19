#!/usr/bin/env python3
"""P14 initial GPT-6 source-only candidate, no hidden test/gold data.

Supports one (x,y) positional pair, keeps legacy set_xy1(x,y) calls. It is a
research-generated candidate: synthesized Git author text does not prove an
autonomous software agent performed the change.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess

BASE_SHA = "cf84d9a6410dec07f57916905c9f54bf00d22b2e"
SOURCE_BLOB_SHA = "9629a821368cc66ddf98f31371ef7c0672642ead"
TARGET = "lib/matplotlib/lines.py"

def git(root, *args):
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True).strip()

def main(root):
    if git(root, "rev-parse", "HEAD") != BASE_SHA:
        raise ValueError("Refusing non-frozen Matplotlib base")
    if git(root, "hash-object", TARGET) != SOURCE_BLOB_SHA:
        raise ValueError("Refusing edited/unverified original source file")
    file = root / TARGET
    original = file.read_text(encoding="utf-8")
    one = "    def set_xy1(self, x, y):"
    two = "    def set_xy2(self, x, y):"
    selfxy1 = "        self._xy1 = x, y"
    selfxy2 = "            self._xy2 = x, y"
    if any(original.count(x) != 1 for x in (one,two,selfxy1,selfxy2)):
        raise ValueError("Unexpected target method signatures")
    edited = original.replace(one, "    def set_xy1(self, x, y=None):", 1)
    edited = edited.replace(two, "    def set_xy2(self, x, y=None):", 1)
    edited = edited.replace(selfxy1, "        if y is None:\n            x, y = x\n        self._xy1 = x, y", 1)
    edited = edited.replace(selfxy2, "            if y is None:\n                x, y = x\n            self._xy2 = x, y", 1)
    file.write_text(edited, encoding="utf-8")
    subprocess.run(["python3", "-m", "py_compile", str(file)], check=True)
    subprocess.run(["git", "-C", str(root), "diff", "--check"], check=True)
    changed = git(root, "diff", "--name-only").splitlines()
    if changed != [TARGET]:
        raise ValueError(f"Unexpected changed source files: {changed}")
    print("P14_INITIAL_PATCH_FILE=" + TARGET)
    print("P14_INITIAL_AGENT_AUTHORSHIP=NOT_INDEPENDENTLY_ATTESTED")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    main(parser.parse_args().repo.resolve())
