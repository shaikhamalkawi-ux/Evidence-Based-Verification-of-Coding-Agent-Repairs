#!/usr/bin/env python3
"""GPT-6 authored initial candidate, no gold patch/test_patch consulted.

Task is from the precommitted ten-task SWE-bench-Live feasibility frame.
Patch only the historical source at the frozen base, with Git blob verification.
"""
from pathlib import Path
import argparse
import hashlib

BASE_BLOB_SHA1 = "3f1e5055ee01250e4cc3141fe0ec30c34c1b36f9"
TARGET = "faker/providers/date_time/__init__.py"
OLD = """        elif start_datetime is None and end_datetime is not None:
            start_datetime = datetime(1970, 1, 1, tzinfo=tzutc())
"""
NEW = """        elif start_datetime is None and end_datetime is not None:
            # A relative end is relative to the current time, not the Unix epoch.
            # Resolve it before installing the default absolute start boundary.
            if not self._is_absolute(end_datetime):
                end_datetime = self._parse_date_time(
                    end_datetime, datetime.now(tz=tzutc()), tzinfo=tzutc()
                )
            start_datetime = datetime(1970, 1, 1, tzinfo=tzutc())
"""

def apply(root):
    fp=Path(root)/TARGET
    raw=fp.read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    if blob != BASE_BLOB_SHA1:
        raise ValueError(f"Original source blob mismatch, expected {BASE_BLOB_SHA1} got {blob}")
    src=raw.decode("utf-8")
    if src.count(OLD)!=1:
        raise ValueError("Expected original unix_time branch not found exactly once")
    fp.write_text(src.replace(OLD,NEW),encoding="utf-8",newline="")
    return fp

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--repo",required=True)
    args=a.parse_args()
    print("Updated",apply(args.repo))
