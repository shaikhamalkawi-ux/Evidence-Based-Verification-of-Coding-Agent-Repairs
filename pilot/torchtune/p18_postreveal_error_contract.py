"""P18 POST-REVEAL, NEW diagnostic of original source error wording.

Intentionally authored after inspecting original SWE-bench-Live F2P failure.
It is NOT preregistered blind/independent verification or proof of DoRA training.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
import sys
import unittest

import torch

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("p17_original_source_ast",HERE/"p17_visible_original_dora_cpu.py")
source=importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)


class P18PostRevealErrorContract(unittest.TestCase):
    def test_original_source_all_meta_parameters_explicitly_rejected(self):
        with torch.device("meta"):
            layer=source.DoRALinear(in_dim=8,out_dim=6,rank=2,alpha=4.0)
        self.assertTrue(layer.magnitude.is_meta)
        with self.assertRaisesRegex(RuntimeError,"Cannot initialize DoRA magnitude"):
            layer.initialize_dora_magnitude()


if __name__=="__main__":
    unittest.main()
