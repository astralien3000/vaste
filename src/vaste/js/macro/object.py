from .macro import *
from vaste import js
from vaste import py


class ObjectJsMacro(JsMacro):

    def __init__(self, name):
        self.name = name

    def match(self, path, py_ast):
        return py.ast.dump(py_ast) == py.ast.dump(path2ast(path))

    class Transformer(JsMacro.Transformer):

        def transform(self, _):
            return js.ast.Identifier(object.__getattribute__(self.macro, "name"))

    def __repr__(self):
        return f"""ObjectJsMacro(name={
            repr(object.__getattribute__(self, "name"))
        })"""

    def __getattribute__(self, k):
        return self

    def __call__(self, *args):
        return self
