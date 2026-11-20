#!/usr/bin/env python3
"""P22 exact issue-visible Reflex/Pydantic Field foreach reproduction.

Runs from historically pinned source checkout installed in runner; no SWE-bench
test_patch, reference fix, hidden oracle, candidate patch, human coder or
unverifiable task-success label. This is a PREPATCH VISIBLE diagnostic only.
"""
from __future__ import annotations

import json
import os
import platform
import sys
import traceback
from pathlib import Path
from datetime import datetime,timezone

TASK="reflex-dev__reflex-4510"


def attempt():
    import reflex as rx
    from pydantic.v1 import Field
    class Tag(rx.Base):
        name: str = ""
    class State(rx.State):
        tags: list[Tag] = Field(default_factory=list)
    def index() -> rx.Component:
        return rx.container(
            rx.foreach(State.tags, lambda tag: rx.text(tag.name))
        )
    app=rx.App()
    app.add_page(index)
    return {"status":"BASELINE_REPRODUCER_NO_EXCEPTION",
            "reflex_version":getattr(rx,"__version__","unknown")}


def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    meta={
        "task":TASK,
        "stage":"HISTORICAL_ORIGINAL_BASE_VISIBLE_ONLY",
        "source_base_sha":"2520c51aaf4c0a4af965026ae3a3fd5b03930288",
        "runner_python":sys.version.split()[0],
        "platform":platform.platform(),
        "original_hidden_oracle_accessed":False,
        "original_source_modified":False,
        "agent_patch_submitted":False,
        "original_test_patch_read":False,
        "started_utc":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
    }
    try:
        meta.update(attempt())
    except Exception as ex:
        text=str(ex)
        meta.update({
            "status":"BASELINE_REPRODUCER_EXCEPTION",
            "exception_type":type(ex).__name__,
            "exception_message":text[:600],
            "reported_original_issue_signature_matches":
               type(ex).__name__=="TypeError" and
               ("annotation" in text.lower() or "Any" in text),
            "traceback_file_names":[Path(f.filename).name for f in traceback.extract_tb(ex.__traceback__)[-8:]],
        })
    meta["completed_utc"]=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(meta,indent=2,sort_keys=True)+"\n")
    print("P22_HISTORICAL_VISIBLE_RESULT "+json.dumps(meta,sort_keys=True))


if __name__=="__main__":
    main()
