#!/usr/bin/env python3
"""GPT-6 initial, source-bounded candidate for python-babel__babel-1163.

No task reference patch, hidden test file, final PR, or post-feedback data was read.
This is the initial candidate, not a certified corrective episode.
"""
from pathlib import Path
import argparse
import subprocess

BASE="fb8dbba89cfc8d8a54d4c34c60b38fd504c4906e"
ORIGINAL_BLOB="5a5b541ad0a5f981eb649605d913354c1cba76fd"

OLD="""        if add_direction:
            unit_rel_patterns = locale._data['date_fields'][a_unit]
            if seconds >= 0:
                yield unit_rel_patterns['future']
            else:
                yield unit_rel_patterns['past']
"""

NEW="""        if add_direction:
            # Respect the requested relative-time width, falling back to the
            # long relative form when a locale lacks a compact field.
            relative_key = a_unit if format == 'long' else f'{a_unit}-{format}'
            fields = locale._data['date_fields']
            unit_rel_patterns = fields.get(relative_key) or fields[a_unit]
            if seconds >= 0:
                yield unit_rel_patterns['future']
            else:
                yield unit_rel_patterns['past']
"""

def apply(repo: Path) -> None:
    path=Path(repo).resolve()
    head=subprocess.check_output(["git","-C",str(path),"rev-parse","HEAD"],text=True).strip()
    if head!=BASE:raise ValueError("Mismatch from frozen base SHA")
    blob=subprocess.check_output(["git","-C",str(path),"hash-object","babel/dates.py"],text=True).strip()
    if blob!=ORIGINAL_BLOB:raise ValueError("Mismatch from frozen dates.py blob SHA")
    dst=path/"babel"/"dates.py"
    s=dst.read_text(encoding="utf-8")
    if s.count(OLD)!=1:raise ValueError("Old relative-pattern block not unique")
    dst.write_text(s.replace(OLD,NEW),encoding="utf-8")
    print("GPT-6 initial Babel width candidate, exactly one source file changed")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo",type=Path,required=True)
    apply(p.parse_args().repo)
