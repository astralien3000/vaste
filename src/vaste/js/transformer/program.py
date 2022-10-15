from .macro import *

import ast


class ProgramTransformer(MacroExpansionTransformer):

    def __init__(self, cls):
        super().__init__(cls)

    def transform(self, py_ast):
        match py_ast:
            case ast.Module(body):
                return js.ast.Program([
                    self.transform_stmt(stmt)
                    for stmt in body
                ])
        return MacroExpansionTransformer.transform(self, py_ast)

    def transform_stmt(self, stmt):
        match stmt:
            case ast.Assign([target], value):
                return js.ast.ExportNamedDeclaration(
                    declarations=[
                        js.ast.VariableDeclarator(
                            id=self.transform(target),
                            init=self.transform(value),
                        )
                    ],
                )
        return self.transform(stmt)
