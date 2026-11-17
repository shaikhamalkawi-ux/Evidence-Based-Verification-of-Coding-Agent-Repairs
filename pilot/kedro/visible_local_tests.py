"""Visible, prespecified (not held-out) checks for the first Kedro feasibility candidate.

This test code evaluates the user-visible alias and lazy import behavior only.
It is not an independent task oracle and is not an official benchmark test patch.
"""
import os
import subprocess
import sys
import types
import unittest

class TestKedroIPythonAlias(unittest.TestCase):
    def test_plain_package_import_remains_lightweight(self):
        subprocess.run([sys.executable, "-c",
            "import kedro,sys;assert 'kedro.ipython' not in sys.modules;"
            "assert callable(kedro.load_ipython_extension)"],
            env=os.environ.copy(),check=True,capture_output=True,text=True)

    def test_public_entry_point_delegates_to_lazy_module(self):
        import kedro
        fake=types.ModuleType("kedro.ipython")
        calls=[]
        fake.load_ipython_extension=lambda shell: calls.append(shell)
        original=sys.modules.get("kedro.ipython")
        original_attr=getattr(kedro,"ipython",None)
        sys.modules["kedro.ipython"]=fake
        setattr(kedro,"ipython",fake)
        try:
            token=object()
            kedro.load_ipython_extension(token)
            self.assertEqual(calls,[token])
        finally:
            if original is None:sys.modules.pop("kedro.ipython",None)
            else:sys.modules["kedro.ipython"]=original
            if original_attr is None:delattr(kedro,"ipython")
            else:setattr(kedro,"ipython",original_attr)

    def test_top_level_alias_signature_has_one_parameter(self):
        import inspect,kedro
        sig=inspect.signature(kedro.load_ipython_extension)
        self.assertEqual(list(sig.parameters),["ipython"])

if __name__=="__main__":
    unittest.main()
