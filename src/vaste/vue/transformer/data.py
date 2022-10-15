from vaste.js.transformer.default import *


class DataTransformer(DefaultTransformer):

    def transform(self, py_ast):
        match py_ast:
            case ast.Module([
                ast.If(
                    ast.Constant(True),
                    [ast.FunctionDef(
                        "data",
                        ast.arguments([], [ast.arg("self")]),
                        body,
                    )]
                )
            ]):
                return js.ast.Property(
                    key=js.ast.Identifier("data"),
                    value=js.ast.FunctionExpression(
                        js.ast.BlockStatement([
                            js.ast.ReturnStatement(
                                js.ast.ObjectExpression([
                                    self.transform(stmt)
                                    for stmt in body
                                ]),
                            ),
                        ]),
                    ),
                    method=True,
                )
            case ast.Assign(
                [ast.Attribute(ast.Name("self"), key)],
                value
            ):
                return js.ast.Property(
                    key=js.ast.Identifier(key),
                    value=self.transform(value),
                )
        return DefaultTransformer.transform(self, py_ast)
