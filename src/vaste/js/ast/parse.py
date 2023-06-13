from . import ast as _ast

import esprima as _esprima
import esprima.nodes as _nodes

from dataclasses import fields as _fields
from types import NoneType as _NoneType
from typing import Literal as _Literal


def _transform(
    ast_node: _nodes.Node|list[_nodes.Node]|str|int|float|_NoneType
) -> _ast.AST|list[_ast.AST]|str|int|float|_NoneType:
    match ast_node:
        case _nodes.Node():
            js_ast_type = getattr(_ast, ast_node.type)
            return js_ast_type(**{
                k: _transform(getattr(ast_node, k))
                for k in ast_node.keys()
                if k in [
                    f.name
                    for f in _fields(js_ast_type)
                ]
            })
        case list():
            return [
                _transform(sub_dict)
                for sub_dict in ast_node
            ]
        case str()|int()|float()|_NoneType():
            return ast_node
        case _:
            raise TypeError(f"Unsupported parsed type {type(ast_node)}")


def parse(
    source: str,
    filename: str = "<unknown>",
    mode: str = _Literal["exec","eval"],
) -> _ast.AST:
    return _transform(
        _esprima.parse(source)
    )
