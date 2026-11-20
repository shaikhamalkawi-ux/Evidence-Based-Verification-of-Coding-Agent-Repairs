#!/usr/bin/env python3
"""P19 first DSPy source candidate: typed LIST demonstration serialization.

Source-only, hypothesis-based; no original SWE-bench gold/test_patch, no
Databricks LM calls, and no independent model-author attestation.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess

BASE_SHA="16ceaba5f7126ca86e5b50b669975c926b9f8f55"
BLOB="5a20dcff321e3aded9c32039d9c060aa79a5e1ea"
TARGET="dspy/adapters/chat_adapter.py"
OLD='        field_names, values = list(signature.output_fields.keys()) + ["completed"], {**values, "completed": ""}'
NEW='''        field_names, values = list(signature.output_fields.keys()) + ["completed"], {**values, "completed": ""}
        # TypedPredictor validates outputs using a JSON parser. During
        # optimization, demonstrations carry already-parsed Python lists;
        # format those typed output values as JSON rather than as the generic
        # human-readable list display used by untyped demonstrations.
        for name, field in signature.output_fields.items():
            if (
                name in values
                and isinstance(values[name], (list, tuple))
                and (field.json_schema_extra or {}).get("parser") is not None
            ):
                values[name] = TypeAdapter(field.annotation).dump_json(values[name]).decode("utf-8")'''


def git(root,*args):
    return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()


def main(root):
    if git(root,"rev-parse","HEAD")!=BASE_SHA:
        raise ValueError("Refuse non-frozen DSPy source base")
    if git(root,"hash-object",TARGET)!=BLOB:
        raise ValueError("Refuse modified historical source blob")
    file=root/TARGET
    source=file.read_text(encoding="utf-8")
    if source.count(OLD)!=1:
        raise ValueError("Original ChatAdapter output demonstration block missing or repeated")
    file.write_text(source.replace(OLD,NEW,1),encoding="utf-8")
    subprocess.run(["python3","-m","py_compile",str(file)],check=True)
    subprocess.run(["git","-C",str(root),"diff","--check"],check=True)
    if git(root,"diff","--name-only").splitlines()!=[TARGET]:
        raise ValueError("P19 candidate modifies an out-of-scope source file")
    print("P19_FIRST_SOURCE_PATCH=CHAT_ADAPTER_TYPED_DEMOS_ONLY")
    print("P19_UNTYPED_OUTPUT_FORMAT=UNCHANGED")
    print("P19_REMOTE_LM_TASK=NOT_REPRODUCED")
    print("P19_AUTHORSHIP_INDEPENDENTLY_ATTESTED=FALSE")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo",type=Path,required=True)
    main(p.parse_args().repo.resolve())
