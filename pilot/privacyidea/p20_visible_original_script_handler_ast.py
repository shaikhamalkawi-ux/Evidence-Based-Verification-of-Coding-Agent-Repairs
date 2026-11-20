"""P20 ten preregistered historical ScriptEventHandler source AST checks.

Compiles the original class AST from exact pinned source; uses standard-library
temporary directories and import-only application bindings. No Flask or DB
endpoint is executed, and no scripts are invoked. Not original hidden oracle.
"""
from __future__ import annotations

import ast
import logging
import os
import subprocess
import traceback
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


SOURCE_ROOT=Path(os.environ["P20_PRIVACYIDEA_SOURCE_ROOT"]).resolve()
SOURCE_PATH=SOURCE_ROOT/"privacyidea/lib/eventhandler/scripthandler.py"


class _BaseEventHandler:
    pass


class _ServerError(Exception):
    pass


def load_original_handler():
    tree=ast.parse(SOURCE_PATH.read_text(encoding="utf-8"),filename=str(SOURCE_PATH))
    nodes=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="ScriptEventHandler"]
    assert len(nodes)==1
    scope={
      "BaseEventHandler":_BaseEventHandler,
      "get_app_config_value":lambda name, default:default,
      "ServerError":_ServerError,
      "is_true":bool,
      "_":lambda x:x,
      "db":type("DB",(),{"session":type("Session",(),{"commit":lambda self:None})()})(),
      "logging":logging,
      "log":logging.getLogger("P20.historical_script_handler"),
      "SCRIPT_BACKGROUND":"background",
      "SCRIPT_WAIT":"wait",
      "subprocess":subprocess,
      "os":os,
      "traceback":traceback,
    }
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SOURCE_PATH),"exec"),scope)
    return scope["ScriptEventHandler"],scope


Handler, SCOPE=load_original_handler()


class OriginalSourceScriptActionsTests(unittest.TestCase):
    def test_nonexistent_script_directory_yields_empty_actions(self):
        with TemporaryDirectory() as root:
            broken=str(Path(root)/"intentionally_missing")
            obj=Handler(script_directory=broken)
            self.assertEqual(obj.actions,{})

    def test_file_as_script_directory_yields_empty_actions(self):
        with TemporaryDirectory() as root:
            not_directory=Path(root)/"config_is_regular_file"
            not_directory.write_text("not a directory")
            obj=Handler(script_directory=str(not_directory))
            self.assertEqual(obj.actions,{})

    def test_permission_error_listing_returns_empty_actions_and_warns(self):
        with TemporaryDirectory() as root:
            obj=Handler(script_directory=root)
            with patch.object(SCOPE["os"],"listdir",side_effect=PermissionError("access denied")):
                with self.assertLogs("P20.historical_script_handler",level="WARNING") as msgs:
                    self.assertEqual(obj.actions,{})
                self.assertIn(root,"\n".join(msgs.output))

    def test_missing_directory_warning_identifies_config_path(self):
        with TemporaryDirectory() as root:
            broken=str(Path(root)/"missing_with_log")
            obj=Handler(script_directory=broken)
            with self.assertLogs("P20.historical_script_handler",level="WARNING") as msgs:
                self.assertEqual(obj.actions,{})
            self.assertIn(broken,"\n".join(msgs.output))

    def test_valid_single_script_listed_without_execution(self):
        with TemporaryDirectory() as root:
            (Path(root)/"run.sh").write_text("#!/bin/sh\nexit 0\n")
            obj=Handler(script_directory=root)
            with patch.object(SCOPE["subprocess"],"Popen",side_effect=AssertionError("must not launch script")):
                actions=obj.actions
            self.assertIn("run.sh",actions)

    def test_valid_two_script_names_preserved(self):
        with TemporaryDirectory() as root:
            for name in ["alpha.sh","beta.sh"]:
                (Path(root)/name).write_text("#!/bin/sh\n")
            out=Handler(script_directory=root).actions
            self.assertEqual(set(out),{"alpha.sh","beta.sh"})

    def test_valid_empty_directory_still_returns_empty_mapping(self):
        with TemporaryDirectory() as root:
            self.assertEqual(Handler(script_directory=root).actions,{})

    def test_successful_action_options_preserve_original_keys_and_values(self):
        with TemporaryDirectory() as root:
            (Path(root)/"job.sh").write_text("#!/bin/sh\n")
            opts=Handler(script_directory=root).actions["job.sh"]
            self.assertEqual(set(opts),{
              "background","raise_error","sync_to_database",
              "serial","user","realm","logged_in_user","logged_in_role",
            })
            self.assertEqual(opts["background"]["value"],["background","wait"])
            self.assertEqual(opts["raise_error"]["visibleValue"],"wait")

    def test_directory_listing_does_not_spawn_process_even_if_two_scripts(self):
        with TemporaryDirectory() as root:
            for name in ["a.sh","b.sh"]:
                (Path(root)/name).write_text("#!/bin/sh\n")
            with patch.object(SCOPE["subprocess"],"Popen") as popen:
                out=Handler(script_directory=root).actions
                self.assertEqual(len(out),2)
                popen.assert_not_called()

    def test_missing_directory_can_be_created_and_recovers_next_listing(self):
        with TemporaryDirectory() as root:
            path=Path(root)/"appears_later"
            obj=Handler(script_directory=str(path))
            self.assertEqual(obj.actions,{})
            path.mkdir()
            (path/"later.sh").write_text("#!/bin/sh\n")
            self.assertIn("later.sh",obj.actions)


if __name__=="__main__":
    unittest.main()
