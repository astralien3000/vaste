from .macro import *

from vaste import py


class ProgramTranspiler(MacroExpansionTranspiler):
    def __init__(self, cls):
        super().__init__(cls)

    def transpile(self, py_ast):
        match py_ast:
            case py.ast.Module(body):
                return js.ast.Program([self.transpile_stmt(stmt) for stmt in body])
        return MacroExpansionTranspiler.transpile(self, py_ast)

    def transpile_stmt(self, stmt):
        match stmt:
            case py.ast.Assign([target], value):
                return js.ast.ExportNamedDeclaration(
                    declarations=[
                        js.ast.VariableDeclaration(
                            [
                                js.ast.VariableDeclarator(
                                    id=self.transpile(target),
                                    init=self.transpile(value),
                                ),
                            ]
                        ),
                    ],
                )
            case py.ast.FunctionDef(name, py.ast.arguments([], [*args]), body, []):
                return js.ast.ExportNamedDeclaration(
                    declarations=[
                        js.ast.FunctionDeclaration(
                            id=js.ast.Identifier(name),
                            params=[self.transpile(arg) for arg in args],
                            body=js.ast.BlockStatement(
                                [self.transpile(stmt) for stmt in body]
                            ),
                        ),
                    ],
                )
        return self.transpile(stmt)
