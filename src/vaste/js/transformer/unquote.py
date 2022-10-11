from .default import *


class UnquoteTransformer(DefaultTransformer):

    def __init__(self, unquote, unquote_name):
        self.unquote = unquote
        self.unquote_name = unquote_name

    def transform(self, py_ast):
        match py_ast:
            case ast.Call(ast.Name(self.unquote_name)):
                return self.unquote.pop()
        return DefaultTransformer.transform(self, py_ast)
