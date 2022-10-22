from .macro import *
from vaste import js


class ObjectJsMacro(JsMacro):

    def __init__(self, name):
        self.name = name

    def match(self, path, py_ast):
        return ast.dump(py_ast) == ast.dump(path2ast(path))

    class Transformer(JsMacro.Transformer):

        def transform(self, _):
            return js.ast.Identifier(self.macro.name)

    def __repr__(self):
        return f"""ObjectJsMacro(name={
            repr(self.name)
        })"""
