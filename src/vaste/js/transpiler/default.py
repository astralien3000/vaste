from vaste import py
from vaste import js

from .transpiler import Transpiler
from vaste.js.transpiler.middleware.default import default


class DefaultTranspiler(Transpiler):
    def error(self, py_ast):
        raise Exception(f"Unmatched ast : {py.ast.dump(py_ast)}")

    def transpile(self, py_ast: py.ast.AST) -> js.ast.AST:
        return default(
            py_ast,
            self.transpile,
            self.error,
        )
