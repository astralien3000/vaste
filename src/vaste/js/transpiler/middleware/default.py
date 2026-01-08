from vaste import py
from vaste import js

from vaste.js.transpiler.middleware.middleware import (
    transpiler_middleware,
    TanspileFunction,
)


@transpiler_middleware
def default(
    py_ast: py.ast.AST,
    transpile: TanspileFunction,
    next: TanspileFunction,
) -> js.ast.AST:
    match py_ast:
        case py.ast.Module(body):
            return js.ast.Program([transpile(stmt_ast) for stmt_ast in body])
        case py.ast.Expr(value):
            return js.ast.ExpressionStatement(transpile(value))
        case py.ast.Call(func, args, []):
            return js.ast.CallExpression(
                callee=transpile(func),
                arguments=[transpile(expr_ast) for expr_ast in args],
            )
        case py.ast.Attribute(value, attr):
            return js.ast.MemberExpression(
                object=transpile(value),
                property=js.ast.Identifier(attr),
            )
        case py.ast.Subscript(value, attr):
            return js.ast.MemberExpression(
                object=transpile(value),
                property=transpile(attr),
                computed=True,
            )
        case py.ast.Name(id):
            return js.ast.Identifier(
                name=id,
            )
        case py.ast.Constant(value):
            return js.ast.Literal(value=value)
        case py.ast.FunctionDef(name, py.ast.arguments([], [*args]), body, []):
            return js.ast.FunctionDeclaration(
                id=js.ast.Identifier(name),
                params=[transpile(arg) for arg in args],
                body=js.ast.BlockStatement([transpile(stmt) for stmt in body]),
            )
        case py.ast.Lambda(py.ast.arguments([], [*args]), body):
            return js.ast.ArrowFunctionExpression(
                params=[transpile(arg) for arg in args],
                body=transpile(body),
            )
        case py.ast.arg(name):
            return js.ast.Identifier(name)
        case py.ast.Return(value):
            return js.ast.ReturnStatement(transpile(value))
        case py.ast.BinOp(left, op, right):
            return js.ast.BinaryExpression(
                left=transpile(left),
                operator=transpile(op),
                right=transpile(right),
            )
        case py.ast.Add():
            return "+"
        case py.ast.Assign([target], value):
            return js.ast.ExpressionStatement(
                js.ast.AssignmentExpression(
                    left=transpile(target),
                    operator="=",
                    right=transpile(value),
                ),
            )
        case py.ast.List(elts):
            return js.ast.ArrayExpression([transpile(elt) for elt in elts])
        case py.ast.ListComp(elt, generators):
            return js.ast.CallExpression(
                callee=js.ast.MemberExpression(
                    object=transpile(generators[-1].iter),
                    property=js.ast.Identifier("map"),
                ),
                arguments=[
                    js.ast.ArrowFunctionExpression(
                        params=[transpile(generators[-1].target)],
                        body=transpile(elt),
                    )
                ],
            )
        case py.ast.Dict(keys, values):
            return js.ast.ObjectExpression(
                [
                    js.ast.Property(
                        key=transpile(key),
                        value=transpile(value),
                    )
                    for key, value in zip(keys, values)
                ]
            )
        case py.ast.If(test, body, orelse):
            return js.ast.IfStatement(
                test=transpile(test),
                consequent=js.ast.BlockStatement([transpile(stmt) for stmt in body]),
                alternate=js.ast.BlockStatement([transpile(stmt) for stmt in orelse]),
            )
        case py.ast.UnaryOp(op, operand):
            return js.ast.UnaryExpression(
                operator=transpile(op),
                argument=transpile(operand),
            )
        case py.ast.Not():
            return "!"
    return next(py_ast)
