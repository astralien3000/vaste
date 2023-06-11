from vaste.js.transformer.macro import *


class RenderTransformer(MacroExpansionTransformer):

    def transform(self, py_ast):
        match py_ast:
            case py.ast.Module([
                py.ast.If(
                    py.ast.Constant(True),
                    [py.ast.FunctionDef(
                        "render",
                        py.ast.arguments([], [py.ast.arg("self")]),
                        body,
                    )]
                )
            ]):
                return js.ast.Property(
                    key=js.ast.Identifier("render"),
                    value=js.ast.FunctionExpression(
                        js.ast.BlockStatement([
                            self.transform(stmt)
                            for stmt in body
                        ]),
                    ),
                    method=True,
                )
            case py.ast.Name("self"):
                return js.ast.Identifier(
                    name="this",
                )
        return MacroExpansionTransformer.transform(self, py_ast)
