#!/usr/bin/env python3
"""P20 first privacyIDEA ScriptEventHandler missing-directory source candidate.

Scoped to the original historical actions property, not the Flask/HTTP route
or script execution code. Neither a full task-resolution claim nor a live app.
"""
from pathlib import Path
import subprocess,argparse

BASE_SHA="a44f38b40a61c5b91e6de68d20d27ed01d3ccb56"
SOURCE_BLOB="ada40e1d3d5284743ae5b3e84c472f20363f4923"
TARGET="privacyidea/lib/eventhandler/scripthandler.py"
OLD="        scripts = os.listdir(cls.script_directory)"
NEW="""        try:
            scripts = os.listdir(cls.script_directory)
        except OSError as error:
            # A missing, invalid, or inaccessible configured script directory
            # must not crash the list of available script event actions.
            log.warning("Cannot list script directory %r: %s",
                        cls.script_directory, error)
            return {}"""


def git(root,*args):
    return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()


def main(root):
    if git(root,"rev-parse","HEAD")!=BASE_SHA:
        raise ValueError("Wrong original privacyIDEA source SHA")
    if git(root,"hash-object",TARGET)!=SOURCE_BLOB:
        raise ValueError("Wrong original ScriptEventHandler source blob")
    f=root/TARGET
    original=f.read_text(encoding="utf-8")
    if original.count(OLD)!=1:
        raise ValueError("Original actions listdir anchor missing or repeated")
    f.write_text(original.replace(OLD,NEW,1),encoding="utf-8")
    subprocess.run(["python3","-m","py_compile",str(f)],check=True)
    subprocess.run(["git","-C",str(root),"diff","--check"],check=True)
    if git(root,"diff","--name-only").splitlines()!=[TARGET]:
        raise ValueError("P20 patch modified an unrelated source")
    print("P20_PATCH_ONLY_ORIGINAL_ACTIONS_LISTDIR_ERROR_RECOVERY")
    print("P20_SCRIPT_EXECUTION_OR_FLASK_ROUTE_NOT_CHANGED")
    print("P20_FULL_HTTP_TASK_NOT_CLAIMED_FIXED")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo",required=True,type=Path)
    main(p.parse_args().repo.resolve())
