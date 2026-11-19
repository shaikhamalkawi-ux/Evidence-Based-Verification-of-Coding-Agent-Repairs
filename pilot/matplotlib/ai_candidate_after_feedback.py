#!/usr/bin/env python3
"""P14 stage-2 code amendment after a real, pre-frozen visible-test failure.

The feedback is synthetic (AI-written) and does not establish independent agent
autonomy. Only the historical lines.py source may change. No benchmark oracle
or gold/test_patch is imported.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

INITIAL_SHA = "ad65fe2531ce297d5770257370b469b80731a614"
TARGET = "lib/matplotlib/lines.py"

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()

def main(root):
    if git(root, "rev-parse", "HEAD") != INITIAL_SHA:
        raise ValueError("Second correction requires EXACT first-stage candidate SHA")
    file = root / TARGET
    orig = file.read_text(encoding="utf-8")
    rules = (
       ("    def set_xy1(self, x, y=None):",
        "    def set_xy1(self, xy, y=None):"),
       ("    def set_xy2(self, x, y=None):",
        "    def set_xy2(self, xy, y=None):"),
       ("        if y is None:\n            x, y = x\n        self._xy1 = x, y",
        "        if y is None:\n            x, y = xy\n        else:\n            x = xy\n        self._xy1 = x, y"),
       ("            if y is None:\n                x, y = x\n            self._xy2 = x, y",
        "            if y is None:\n                x, y = xy\n            else:\n                x = xy\n            self._xy2 = x, y"),
    )
    for old, new in rules:
        if orig.count(old) != 1:
            raise ValueError("Unexpected or repeated source anchor: " + old.split("\n")[0])
        orig = orig.replace(old, new, 1)
    file.write_text(orig, encoding="utf-8")
    subprocess.run(["python3", "-m", "py_compile", str(file)], check=True)
    subprocess.run(["git", "-C", str(root), "diff", "--check"], check=True)
    changed = git(root, "diff", "--name-only").splitlines()
    if changed != [TARGET]:
        raise ValueError(f"Unexpected stage-2 file modifications: {changed}")
    print("P14_STAGE2_SAME_SOURCE_FILE=" + TARGET)
    print("P14_STAGE2_CORRECTION_TARGET=xy_keyword_and_legacy_compatibility")
    print("P14_STAGE2_HUMAN_DEVELOPER_FEEDBACK=FALSE")
    print("P14_STAGE2_HIDDEN_ORACLE_SEEN=FALSE")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    main(p.parse_args().repo.resolve())
