"""P17 pre-frozen CPU verification of the ORIGINAL historical DoRALinear class.

Read the original, exact blob-verified torchtune/modules/peft/dora.py; compile its
unchanged class and two private init helpers from its actual AST. Minimal stub
names only replace import-only dependencies (torchao, torchtune modules) that
are not invoked for unquantized DoRA. NOT a full original torchao/FSDP import,
distributed training, or SWE-bench-Live independent task oracle.

The same tests must be run on BOTH unchanged base and candidate. Tests are
saved before the first P17 candidate is generated.
"""
from __future__ import annotations

import ast
import math
import os
from pathlib import Path
from typing import List
import unittest

import torch
from torch import nn
import torch.nn.functional as F


SOURCE_ROOT=Path(os.environ["P17_TORCHTUNE_SOURCE_ROOT"]).resolve()
SOURCE_FILE=SOURCE_ROOT/"torchtune/modules/peft/dora.py"


class AdapterModule:
    """Import-only stand-in for the original Protocol type; no functionality."""


def _reject_quantized_branch(*_args, **_kwargs):
    raise RuntimeError("Quantized torchtune/torchao path is OUTSIDE P17 CPU scope")


def original_dora_class():
    src=SOURCE_FILE.read_text(encoding="utf-8")
    ast_tree=ast.parse(src,filename=str(SOURCE_FILE))
    selected=[]
    for n in ast_tree.body:
        if isinstance(n,ast.ClassDef) and n.name=="DoRALinear":
            selected.append(n)
        if isinstance(n,ast.FunctionDef) and n.name in ("_lora_a_init_params","_lora_b_init_params"):
            selected.append(n)
    assert len(selected)==3
    globals_={
        "__name__":"P17_historical_DORA_AST_ONLY",
        "torch":torch,"nn":nn,"F":F,"math":math,"List":List,
        "AdapterModule":AdapterModule,
        "to_nf4":_reject_quantized_branch,
        "linear_nf4":_reject_quantized_branch,
    }
    # Original source AST nodes are NEVER edited; only import-only bindings are stubbed.
    compiled=compile(ast.Module(body=selected,type_ignores=[]),str(SOURCE_FILE),"exec")
    exec(compiled,globals_)
    return globals_["DoRALinear"]


DoRALinear=original_dora_class()


def model():
    torch.manual_seed(29)
    return DoRALinear(in_dim=8,out_dim=6,rank=2,alpha=4.0,dropout=0.0,use_bias=False)


class TestHistoricalOriginalDoRAMagnitudeCPU(unittest.TestCase):
    def test_induced_stale_meta_magnitude_is_materialized(self):
        m=model()
        # Original base/LoRA are real CPU tensors; DoRA magnitude is still meta.
        m.magnitude=nn.Parameter(torch.empty(m.out_dim,device="meta"))
        self.assertTrue(m.magnitude.is_meta)
        m.initialize_dora_magnitude()
        self.assertFalse(m.magnitude.is_meta,"Original copy_ on meta must be fixed")
        self.assertEqual(str(m.magnitude.device),"cpu")

    def test_calculated_magnitude_not_merely_uninitialized_storage(self):
        m=model()
        base=m.weight.detach().clone()
        lora=m.lora_b.weight.detach()@m.lora_a.weight.detach()
        expected=torch.linalg.vector_norm(base+m.scaling*lora,dim=1)
        m.magnitude=nn.Parameter(torch.empty(m.out_dim,device="meta"))
        m.initialize_dora_magnitude()
        torch.testing.assert_close(m.magnitude.detach(),expected)

    def test_existing_cpu_parameter_identity_preserved(self):
        m=model()
        param=m.magnitude
        pid=id(param)
        m.initialize_dora_magnitude()
        self.assertIs(m.magnitude,param)
        self.assertEqual(id(m.magnitude),pid)
        self.assertFalse(m.magnitude.is_meta)

    def test_regular_cpu_value_correct_and_reinitialization_stable(self):
        m=model()
        m.initialize_dora_magnitude()
        first=m.magnitude.detach().clone()
        m.initialize_dora_magnitude()
        torch.testing.assert_close(m.magnitude.detach(),first,rtol=0,atol=0)
        self.assertTrue(bool(torch.isfinite(first).all()))

    def test_forward_and_backward_after_meta_recovery(self):
        m=model()
        m.magnitude=nn.Parameter(torch.empty(m.out_dim,device="meta"))
        m.initialize_dora_magnitude()
        x=torch.randn(2,m.in_dim)
        y=m(x)
        self.assertEqual(tuple(y.shape),(2,m.out_dim))
        y.square().mean().backward()
        self.assertIsNotNone(m.magnitude.grad)
        self.assertTrue(bool(torch.isfinite(m.magnitude.grad).all()))
        self.assertEqual(str(m.magnitude.grad.device),"cpu")

    def test_unsharded_state_dict_is_materialized_and_restorable(self):
        m=model()
        m.magnitude=nn.Parameter(torch.empty(m.out_dim,device="meta"))
        m.initialize_dora_magnitude()
        state=m.state_dict()
        self.assertFalse(state["magnitude"].is_meta)
        fresh=model()
        result=fresh.load_state_dict(state,strict=True)
        self.assertEqual(result.missing_keys,[])
        self.assertEqual(result.unexpected_keys,[])
        torch.testing.assert_close(fresh.magnitude.detach(),m.magnitude.detach())


if __name__=="__main__":
    unittest.main()
