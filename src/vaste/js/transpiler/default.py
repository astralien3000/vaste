from vaste import py
from vaste import js


class DefaultTranspiler:

    def transpile(self, py_ast: py.ast.AST) -> js.ast.AST:
        match py_ast:
            case py.ast.Module(body):
                return js.ast.Program([
                    self.transpile(stmt_ast)
                    for stmt_ast in body
                ])
            case py.ast.Expr(value):
                return js.ast.ExpressionStatement(
                    self.transpile(value)
                )
            case py.ast.Call(func, args, []):
                return js.ast.CallExpression(
                    callee=self.transpile(func),
                    arguments=[
                        self.transpile(expr_ast)
                        for expr_ast in args
                    ],
                )
            case py.ast.Attribute(value, attr):
                return js.ast.MemberExpression(
                    object=self.transpile(value),
                    property=js.ast.Identifier(attr),
                )
            case py.ast.Subscript(value, attr):
                return js.ast.MemberExpression(
                    object=self.transpile(value),
                    property=self.transpile(attr),
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
                        self.transpile(arg)
                        for arg in args
                    ],
                    body=js.ast.BlockStatement([
                        self.transpile(stmt)
                        for stmt in body
                    ])
                )
            case py.ast.Lambda(py.ast.arguments([], [*args]), body):
                return js.ast.ArrowFunctionExpression(
                    params=[
                        self.transpile(arg)
                        for arg in args
                    ],
                    body=self.transpile(body),
                )
            case py.ast.arg(name):
                return js.ast.Identifier(name)
            case py.ast.Return(value):
                return js.ast.ReturnStatement(
                    self.transpile(value)
                )
            case py.ast.BinOp(left, op, right):
                return js.ast.BinaryExpression(
                    left=self.transpile(left),
                    operator=self.transpile(op),
                    right=self.transpile(right),
                )
            case py.ast.Add():
                return "+"
            case py.ast.Assign([target], value):
                return js.ast.ExpressionStatement(
                    js.ast.AssignmentExpression(
                        left=self.transpile(target),
                        operator="=",
                        right=self.transpile(value),
                    ),
                )
            case py.ast.List(elts):
                return js.ast.ArrayExpression([
                    self.transpile(elt)
                    for elt in elts
                ])
            case py.ast.ListComp(elt, generators):
                return js.ast.CallExpression(
                    callee=js.ast.MemberExpression(
                        object=self.transpile(generators[-1].iter),
                        property=js.ast.Identifier("map"),
                    ),
                    arguments=[
                        js.ast.ArrowFunctionExpression(
                            params=[
                                self.transpile(generators[-1].target)
                            ],
                            body=self.transpile(elt),
                        )
                    ],
                )
            case py.ast.Dict(keys, values):
                return js.ast.ObjectExpression([
                    js.ast.Property(
                        key=self.transpile(key),
                        value=self.transpile(value),
                    )
                    for key, value in zip(keys, values)
                ])
            case py.ast.If(test, body, orelse):
                return js.ast.IfStatement(
                    test=self.transpile(test),
                    consequent=js.ast.BlockStatement([
                        self.transpile(stmt)
                        for stmt in body
                    ]),
                    alternate=js.ast.BlockStatement([
                        self.transpile(stmt)
                        for stmt in orelse
                    ]),
                )
            case py.ast.UnaryOp(op, operand):
                return js.ast.UnaryExpression(
                    operator=self.transpile(op),
                    argument=self.transpile(operand),
                )
            case py.ast.Not():
                return "!"
        raise Exception(f"Unmatched ast : {py.ast.dump(py_ast)}")
