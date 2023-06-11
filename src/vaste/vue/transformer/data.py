from vaste.js.transformer.default import *


class DataTransformer(DefaultTransformer):

    def transform(self, py_ast):
        match py_ast:
            case py.ast.Module([
                py.ast.If(
                    py.ast.Constant(True),
                    [py.ast.FunctionDef(
                        "data",
                        py.ast.arguments([], [py.ast.arg("self")]),
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
            case py.ast.Assign(
                [py.ast.Attribute(py.ast.Name("self"), key)],
                value
            ):
                return js.ast.Property(
                    key=js.ast.Identifier(key),
                    value=self.transform(value),
                )
        return DefaultTransformer.transform(self, py_ast)
