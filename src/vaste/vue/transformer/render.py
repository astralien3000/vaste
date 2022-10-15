from vaste.js.transformer.macro import *


class RenderTransformer(MacroTransformer):

    def transform(self, py_ast):
        match py_ast:
            case ast.Module([
                ast.If(
                    ast.Constant(True),
                    [ast.FunctionDef(
                        "render",
                        ast.arguments([], [ast.arg("self")]),
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
            case ast.Name("self"):
                return js.ast.Identifier(
                    name="this",
                )
        return MacroTransformer.transform(self, py_ast)
