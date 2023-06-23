from vaste.js.transpiler.macro import *


class DataTranspiler(MacroExpansionTranspiler):
    def transpile(self, py_ast):
        match py_ast:
            case py.ast.Module(
                [
                    py.ast.If(
                        py.ast.Constant(True),
                        [
                            py.ast.FunctionDef(
                                "data",
                                py.ast.arguments([], [py.ast.arg("self")]),
                                body,
                            )
                        ],
                    )
                ]
            ):
                return js.ast.Property(
                    key=js.ast.Identifier("data"),
                    value=js.ast.FunctionExpression(
                        js.ast.BlockStatement(
                            [
                                js.ast.ReturnStatement(
                                    js.ast.ObjectExpression(
                                        [self.transpile(stmt) for stmt in body]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    method=True,
                )
            case py.ast.Assign([py.ast.Attribute(py.ast.Name("self"), key)], value):
                return js.ast.Property(
                    key=js.ast.Identifier(key),
                    value=self.transpile(value),
                )
            case py.ast.Name("self"):
                return js.ast.Identifier(
                    name="this",
                )
        return super().transpile(py_ast)
