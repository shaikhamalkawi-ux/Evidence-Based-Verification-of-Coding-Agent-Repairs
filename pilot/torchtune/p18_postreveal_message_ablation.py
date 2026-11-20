#!/usr/bin/env python3
"""P18 *POST-REVEAL* literal-only source sensitivity ablation.

This patch is written AFTER observing the original SWE-bench-Live F2P regex.
It does not change tensor operations, DoRA math, GPU training or FSDP behavior.
Never interpret any following benchmark PASS as a new blind agent repair.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import subprocess

P17_SHA="57f45fdd5552908d4b5d42cccd7359ccb4de2560"
P17_SOURCE_BLOB="b83691d2a0e5e5aef19259d12fce189c4c1a82a0"
TARGET="torchtune/modules/peft/dora.py"
OLD='raise RuntimeError("DoRA magnitude norm is still on meta device")'
NEW='raise RuntimeError("Cannot initialize DoRA magnitude: computed norm is still on meta device")'


def git(repo,*args):
    return subprocess.check_output(["git","-C",str(repo),*args],text=True).strip()


def main(repo):
    if git(repo,"rev-parse","HEAD")!=P17_SHA:
        raise ValueError("Postreveal P18 must begin from exact original P17 candidate")
    if git(repo,"hash-object",TARGET)!=P17_SOURCE_BLOB:
        raise ValueError("P17 candidate blob changed; refuse postreveal ablation")
    path=repo/TARGET
    text=path.read_text(encoding="utf-8")
    if text.count(OLD)!=1:
        raise ValueError("Original P17 exception literal not unique")
    path.write_text(text.replace(OLD,NEW,1),encoding="utf-8")
    subprocess.run(["python3","-m","py_compile",str(path)],check=True)
    subprocess.run(["git","-C",str(repo),"diff","--check"],check=True)
    if git(repo,"diff","--name-only").splitlines()!=[TARGET]:
        raise ValueError("Only original DoRALinear source text may change")
    print("P18_POSTREVEAL_LITERAL_ONLY_NO_TENSOR_LOGIC_CHANGE")
    print("P18_BLINDED_AGENT_EVIDENCE=FALSE")
    print("P18_DISTRIBUTED_TRAINING_TESTED=FALSE")


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    main(ap.parse_args().repo.resolve())
