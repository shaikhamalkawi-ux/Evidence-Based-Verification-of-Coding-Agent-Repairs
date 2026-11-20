#!/usr/bin/env python3
"""P22B postbaseline exception context; original historical source UNMODIFIED."""
import json
import platform
import sys
import traceback
from pathlib import Path
from datetime import datetime,timezone

def record(e):
    out=[]
    seen=set()
    current=e
    for i in range(7):
        if current is None or id(current) in seen:break
        seen.add(id(current))
        frames=traceback.extract_tb(current.__traceback__)
        out.append({
         "depth":i,
         "type":type(current).__name__,
         "message":str(current)[:440],
         "suppress_context":bool(current.__suppress_context__),
         "frames":[{"file":Path(f.filename).name,"line":f.lineno,"func":f.name} for f in frames[-8:]]
        })
        current=current.__cause__ or current.__context__
    return out

def reproduce():
    from pydantic.v1 import Field
    import reflex as rx
    class Tag(rx.Base):
        name:str=""
    class State(rx.State):
        tags:list[Tag]=Field(default_factory=list)
    def index()->rx.Component:
        return rx.container(rx.foreach(State.tags,lambda tag:rx.text(tag.name)))
    app=rx.App()
    app.add_page(index)

if __name__=="__main__":
    try:
        reproduce()
        trace=[]
        result="NO_EXCEPTION"
    except Exception as ex:
        trace=record(ex)
        result="EXCEPTION_CHAIN_IDENTIFIED"
    obj={
      "schema":"P22B_original_compat_exception_context",
      "status":result,
      "python":sys.version.split()[0],
      "source_sha":"2520c51aaf4c0a4af965026ae3a3fd5b03930288",
      "task":"reflex-dev__reflex-4510",
      "exception_chain":trace,
      "benchmark_oracle_used":False,
      "source_modified":False,
      "is_repair_test":False,
      "time_utc":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
    }
    out=Path("p22b_diag/P22B_CHAIN.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
    print("P22B_EXCEPTION_CHAIN "+json.dumps(obj,sort_keys=True))
