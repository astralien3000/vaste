import ast
import inspect

from vaste.js.macro.macro import JsMacro
from vaste.js.transformer.macro import macro_map


class FindMacroVisitor(ast.NodeVisitor):

    def __init__(self, cls):
        self.macro_map = macro_map(inspect.getmodule(cls))
        self.cache = set()

    def visit(self, py_ast):
        ast.NodeVisitor.visit(self, py_ast)
        return self.cache

    def generic_visit(self, py_ast):
        ast.NodeVisitor.generic_visit(self, py_ast)
        for path, macro in self.macro_map.items():
            if type(macro).match(macro, path, py_ast):
                self.cache.add(macro)
