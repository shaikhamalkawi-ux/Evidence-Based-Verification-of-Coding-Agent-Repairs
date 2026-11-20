"""P19 frozen real historical ChatAdapter AST tests; no live model or benchmark gold.

Compile original ChatAdapter + its helper functions from exact pinned source.
Stub ONLY unrelated package import machinery. Pydantic TypeAdapter is real.
The identical tests run on historic source and the first patch.
"""
from __future__ import annotations

import ast
import json
import os
import re
import textwrap
from pathlib import Path
from typing import List, get_args, get_origin
import unittest
from dataclasses import dataclass

import pydantic
from pydantic import BaseModel, TypeAdapter


SRC = Path(os.environ["P19_DSPY_SOURCE_ROOT"]).resolve() / "dspy/adapters/chat_adapter.py"
FUNCTIONS = {
    "format_blob", "format_list", "_format_field_value", "format_fields",
    "parse_value", "format_turn", "get_annotation_name",
    "enumerate_fields", "prepare_instructions",
}


def load_actual_source():
    tree=ast.parse(SRC.read_text(encoding="utf-8"),filename=str(SRC))
    nodes=[x for x in tree.body if (
       isinstance(x,ast.FunctionDef) and x.name in FUNCTIONS
       or isinstance(x,ast.ClassDef) and x.name=="ChatAdapter")]
    assert {x.name for x in nodes} == FUNCTIONS | {"ChatAdapter"}
    scope={
      "__name__":"P19_HISTORICAL_CHAT_ADAPTER_AST_ONLY",
      "ast":ast, "json":json,"re":re,"textwrap":textwrap,
      "get_args":get_args,"get_origin":get_origin,
      "pydantic":pydantic,"TypeAdapter":TypeAdapter,
      "Adapter":object,
      "field_header_pattern":re.compile(r"\[\[ ## (\w+) ## \]\]"),
    }
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SRC),"exec"),scope)
    return scope


SOURCE=load_actual_source()
format_turn=SOURCE["format_turn"]
ChatAdapter=SOURCE["ChatAdapter"]


@dataclass
class Field:
    annotation: object
    json_schema_extra: dict


class Sig:
    def __init__(self, output_type=List[str], *, typed=True, input_type=str):
        self.instructions="Return the token list."
        self.input_fields={"text":Field(input_type,{"desc":"$"+"{text}"})}
        extra={"desc":"$"+"{tokens}"}
        if typed:
            extra["parser"]=lambda value: TypeAdapter(output_type).validate_json(value)
        self.output_fields={"tokens":Field(output_type,extra)}
        self.fields={**self.input_fields,**self.output_fields}


def output_value(text: str, field="tokens")->str:
    marker=f"[[ ## {field} ## ]]\n"
    if marker not in text:
        raise AssertionError("Output field missing")
    return text.split(marker,1)[1].split("\n\n[[ ## completed ## ]]",1)[0].strip()


class NamedToken(BaseModel):
    token: str
    index: int


class TestOriginalAdapter(unittest.TestCase):
    def test_typing_List_str_output_demo_is_JSON(self):
        sig=Sig(List[str])
        rendered=output_value(format_turn(sig,{"tokens":["EU","rejects"]},"assistant")["content"])
        self.assertEqual(TypeAdapter(List[str]).validate_json(rendered),["EU","rejects"])

    def test_builtin_list_str_output_demo_is_JSON(self):
        sig=Sig(list[str])
        rendered=output_value(format_turn(sig,{"tokens":["British","lamb"]},"assistant")["content"])
        self.assertEqual(TypeAdapter(list[str]).validate_json(rendered),["British","lamb"])

    def test_nested_pydantic_list_demo_roundtrips(self):
        sig=Sig(list[NamedToken])
        expected=[NamedToken(token="Peter",index=0),NamedToken(token="Blackburn",index=1)]
        rendered=output_value(format_turn(sig,{"tokens":expected},"assistant")["content"])
        self.assertEqual(TypeAdapter(list[NamedToken]).validate_json(rendered),expected)

    def test_unicode_quoted_tokens_and_punctuation_roundtrip(self):
        sig=Sig(List[str])
        expected=["don't",'he said "hello"',"BRUSSELS","أبوظبي",",",".","«special»"]
        rendered=output_value(format_turn(sig,{"tokens":expected},"assistant")["content"])
        self.assertEqual(TypeAdapter(List[str]).validate_json(rendered),expected)

    def test_empty_typed_list_is_valid_JSON_not_NA(self):
        sig=Sig(list[str])
        rendered=output_value(format_turn(sig,{"tokens":[]},"assistant")["content"])
        self.assertEqual(rendered,"[]")
        self.assertEqual(TypeAdapter(list[str]).validate_json(rendered),[])

    def test_untyped_list_demo_retains_original_human_readable_format(self):
        sig=Sig(list[str],typed=False)
        rendered=output_value(format_turn(sig,{"tokens":["EU","rejects"]},"assistant")["content"])
        self.assertEqual(rendered,"[1] «EU»\n[2] «rejects»")

    def test_list_input_preserves_original_format(self):
        sig=Sig(list[str],typed=True,input_type=list[str])
        rendered=format_turn(sig,{"text":["EU","rejects"]},"user")["content"]
        self.assertIn("[[ ## text ## ]]\n[1] «EU»\n[2] «rejects»",rendered)

    def test_simple_string_output_unchanged(self):
        sig=Sig(str,typed=True)
        rendered=output_value(format_turn(sig,{"tokens":"EU rejects"},"assistant")["content"])
        self.assertEqual(rendered,"EU rejects")

    def test_entire_ChatAdapter_demonstration_and_parser_roundtrip(self):
        sig=Sig(list[str],typed=True)
        adapter=ChatAdapter()
        messages=adapter.format(sig,[{"text":"EU rejects","tokens":["EU","rejects"]}],{"text":"Peter Blackburn"})
        self.assertEqual([m["role"] for m in messages],["system","user","assistant","user"])
        parsed=adapter.parse(sig,messages[2]["content"],_parse_values=True)
        self.assertEqual(parsed["tokens"],["EU","rejects"])


if __name__=="__main__":
    unittest.main()
