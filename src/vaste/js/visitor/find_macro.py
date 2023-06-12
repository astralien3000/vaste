from vaste import py
from vaste.js.macro.macro import JsMacro
from vaste.js.transformer.macro import macro_map_frame


class FindMacroVisitor(py.ast.NodeVisitor):

    def __init__(self, frame):
        self.macro_map = macro_map_frame(frame)
        self.cache = set()

    def visit(self, py_ast):
        py.ast.NodeVisitor.visit(self, py_ast)
        return self.cache

    def generic_visit(self, py_ast):
        py.ast.NodeVisitor.generic_visit(self, py_ast)
        for path, macro in self.macro_map.items():
            if type(macro).match(macro, path, py_ast):
                self.cache.add(macro)
