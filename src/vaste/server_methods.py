from .js.transformer.default import *


class ServerMethodsTransformer(DefaultTransformer):

    def transform(self, py_ast):
        match py_ast:
            case ast.Module([module_cls]):
                return self.transform(module_cls)
            case ast.ClassDef("module", [], [], [methods_cls], []):
                return self.transform(methods_cls)
            case ast.ClassDef("server_methods", [], [], body, []):
                return js.ast.Property(
                    key=js.ast.Identifier("methods"),
                    value=js.ast.ObjectExpression([
                        self.transform(stmt)
                        for stmt in body
                    ]),
                )
            case ast.FunctionDef(name, ast.arguments([], [ast.arg("self"), *args]), body, []):
                return js.ast.Property(
                    key=js.ast.Identifier(name),
                    value=js.ast.FunctionExpression(
                        params=[
                            self.transform(arg)
                            for arg in args
                        ],
                        body=js.ast.BlockStatement([
                            js.ast.VariableDeclaration(
                                kind="var",
                                declarations=[
                                    js.ast.VariableDeclarator(
                                        id=js.ast.Identifier("xmlHttp"),
                                        init=js.ast.NewExpression(
                                            callee=js.ast.Identifier("XMLHttpRequest"),
                                            arguments=[],
                                        )
                                    )
                                ],
                            ),
                            js.ast.ExpressionStatement(
                                js.ast.CallExpression(
                                    callee=js.ast.MemberExpression(
                                        object=js.ast.Identifier("xmlHttp"),
                                        property=js.ast.Identifier("open"),
                                    ),
                                    arguments=[
                                        js.ast.Literal("GET"),
                                        js.ast.BinaryExpression(
                                            left=js.ast.Literal(f"api/{name}?self="),
                                            operator="+",
                                            right=js.ast.CallExpression(
                                                callee=js.ast.MemberExpression(
                                                    object=js.ast.Identifier("JSON"),
                                                    property=js.ast.Identifier("stringify"),
                                                ),
                                                arguments=[
                                                    js.ast.MemberExpression(
                                                        object=js.ast.Identifier("this"),
                                                        property=js.ast.Identifier("$data"),
                                                    ),
                                                ],
                                            )
                                        ),
                                        js.ast.Literal(False),
                                    ],
                                )
                            ),
                            js.ast.ExpressionStatement(
                                js.ast.CallExpression(
                                    callee=js.ast.MemberExpression(
                                        object=js.ast.Identifier("xmlHttp"),
                                        property=js.ast.Identifier("send"),
                                    ),
                                    arguments=[
                                        js.ast.Literal(None),
                                    ],
                                )
                            ),
                            js.ast.ReturnStatement(
                                js.ast.CallExpression(
                                    callee=js.ast.MemberExpression(
                                        object=js.ast.Identifier("JSON"),
                                        property=js.ast.Identifier("parse"),
                                    ),
                                    arguments=[
                                        js.ast.MemberExpression(
                                            object=js.ast.Identifier("xmlHttp"),
                                            property=js.ast.Identifier("response"),
                                        ),
                                    ],
                                ),
                            ),
                        ])
                    ),
                    method=True,
                )
        return DefaultTransformer.transform(self, py_ast)
