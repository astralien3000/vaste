from vaste import py
from vaste import js


class DefaultTransformer:

    def transform(self, py_ast):
        match py_ast:
            case py.ast.Module(body):
                return js.ast.Program([
                    self.transform(stmt_ast)
                    for stmt_ast in body
                ])
            case py.ast.Expr(value):
                return js.ast.ExpressionStatement(
                    self.transform(value)
                )
            case py.ast.Call(func, args, []):
                return js.ast.CallExpression(
                    callee=self.transform(func),
                    arguments=[
                        self.transform(expr_ast)
                        for expr_ast in args
                    ],
                )
            case py.ast.Attribute(value, attr):
                return js.ast.MemberExpression(
                    object=self.transform(value),
                    property=js.ast.Identifier(attr),
                )
            case py.ast.Subscript(value, attr):
                return js.ast.MemberExpression(
                    object=self.transform(value),
                    property=self.transform(attr),
                    computed=True,
                )
            case py.ast.Name(id):
                return js.ast.Identifier(
                    name=id,
                )
            case py.ast.Constant(value):
                return js.ast.Literal(
                    value=value
                )
            case py.ast.FunctionDef(name, py.ast.arguments([], [*args]), body, []):
                return js.ast.FunctionDeclaration(
                    id=js.ast.Identifier(name),
                    params=[
                        self.transform(arg)
                        for arg in args
                    ],
                    body=js.ast.BlockStatement([
                        self.transform(stmt)
                        for stmt in body
                    ])
                )
            case py.ast.arg(name):
                return js.ast.Identifier(name)
            case py.ast.Return(value):
                return js.ast.ReturnStatement(
                    self.transform(value)
                )
            case py.ast.BinOp(left, op, right):
                return js.ast.BinaryExpression(
                    left=self.transform(left),
                    operator=self.transform(op),
                    right=self.transform(right),
                )
            case py.ast.Add():
                return "+"
            case py.ast.Assign([target], value):
                return js.ast.ExpressionStatement(
                    js.ast.AssignmentExpression(
                        left=self.transform(target),
                        operator="=",
                        right=self.transform(value),
                    ),
                )
            case py.ast.List(elts):
                return js.ast.ArrayExpression([
                    self.transform(elt)
                    for elt in elts
                ])
            case py.ast.ListComp(elt, generators):
                return js.ast.CallExpression(
                    callee=js.ast.MemberExpression(
                        object=self.transform(generators[-1].iter),
                        property=js.ast.Identifier("map"),
                    ),
                    arguments=[
                        js.ast.ArrowFunctionExpression(
                            params=[
                                self.transform(generators[-1].target)
                            ],
                            body=self.transform(elt),
                        )
                    ],
                )
            case py.ast.Dict(keys, values):
                return js.ast.ObjectExpression([
                    js.ast.Property(
                        key=self.transform(key),
                        value=self.transform(value),
                    )
                    for key, value in zip(keys, values)
                ])
        raise Exception(f"Unmatched ast : {py.ast.dump(py_ast)}")
