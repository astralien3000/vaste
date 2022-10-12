from .default import *

from vaste import js


class UnquoteTransformer(DefaultTransformer):

    def __init__(self, unquote, unquote_name):
        self.unquote = unquote
        self.unquote_name = unquote_name

    def transform(self, py_ast):
        match py_ast:
            case ast.Call(ast.Name(self.unquote_name)):
                return self.unquote.pop()
            case ast.Assign(
                [ast.Name(spec_name)],
                ast.Call(
                    ast.Name("jsimport"),
                    [ast.Constant(source)],
                ),
            ):
                return js.ast.ImportDeclaration(
                    specifiers=[
                        js.ast.ImportNamespaceSpecifier(
                            js.ast.Identifier(spec_name),
                        ),
                    ],
                    source=js.ast.Literal(source),
                )
        return DefaultTransformer.transform(self, py_ast)
