#!/usr/bin/env python3
"""P17 first source patch for historical torchtune DoRALinear.

Hypothesis-informed by the earlier disclosed P16 meta toy result. NEVER
described as a full 2-GPU DoRA training repair. No gold/test_patch of the
original SWE-bench-Live task is read by this recipe.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

BASE_SHA="f2bd4bc25b24587aef40f486087412b9da8f1d94"
SOURCE_BLOB_SHA="6f097da6d039738c320e8775ad61950c56fe0108"
TARGET="torchtune/modules/peft/dora.py"
OLD="        self.magnitude.copy_(weight_norm)"
NEW="""        # A copy_ into a meta Parameter is a no-op: it does not materialize it.
        # A new Parameter is needed only in that case; preserve the original
        # object (and any existing optimizer/registration references) otherwise.
        if self.magnitude.is_meta:
            if weight_norm.is_meta:
                raise RuntimeError("DoRA magnitude norm is still on meta device")
            self.magnitude = nn.Parameter(weight_norm.detach())
        else:
            self.magnitude.copy_(weight_norm)
"""


def git(root: Path,*args: str)->str:
    return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()


def main(repo: Path)->None:
    if git(repo,"rev-parse","HEAD")!=BASE_SHA:
        raise ValueError("P17 original source commit differs from frozen base")
    if git(repo,"hash-object",TARGET)!=SOURCE_BLOB_SHA:
        raise ValueError("P17 original DoRA source blob changed")
    target=repo/TARGET
    src=target.read_text(encoding="utf-8")
    if src.count(OLD)!=1:
        raise ValueError("Expected unique historical DoRA copy_ line absent")
    target.write_text(src.replace(OLD,NEW,1),encoding="utf-8")
    subprocess.run(["python3","-m","py_compile",str(target)],check=True)
    subprocess.run(["git","-C",str(repo),"diff","--check"],check=True)
    if git(repo,"diff","--name-only").splitlines()!=[TARGET]:
        raise ValueError("P17 must only modify historical DoRALinear source")
    print("P17_CANDIDATE_CHANGED_ONLY="+TARGET)
    print("P17_DESIGN=CONDITIONAL_META_MATERIALIZATION_PRESERVE_CPU_IDENTITY")
    print("P17_FSDP_GPU_TRAINING=UNTESTED")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo",required=True,type=Path)
    main(p.parse_args().repo.resolve())
