from vaste.js.transpiler.macro import *


class RenderTranspiler(MacroExpansionTranspiler):
    def transpile(self, py_ast):
        match py_ast:
            case py.ast.Module(
                [
                    py.ast.If(
                        py.ast.Constant(True),
                        [
                            py.ast.FunctionDef(
                                "render",
                                py.ast.arguments([], [py.ast.arg("self")]),
                                body,
                            )
                        ],
                    )
                ]
            ):
                return js.ast.Property(
                    key=js.ast.Identifier("render"),
                    value=js.ast.FunctionExpression(
                        js.ast.BlockStatement([self.transpile(stmt) for stmt in body]),
                    ),
                    method=True,
                )
            case py.ast.Name("self"):
                return js.ast.Identifier(
                    name="this",
                )
        return MacroExpansionTranspiler.transpile(self, py_ast)
