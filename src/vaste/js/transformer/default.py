import ast
from vaste import js


class DefaultTransformer:

    def transform(self, py_ast):
        match py_ast:
            case ast.Module(body):
                return js.ast.Program([
                    self.transform(stmt_ast)
                    for stmt_ast in body
                ])
            case ast.Expr(value):
                return js.ast.ExpressionStatement(
                    self.transform(value)
                )
            case ast.Call(func, args):
                return js.ast.CallExpression(
                    callee=self.transform(func),
                    arguments=[
                        self.transform(expr_ast)
                        for expr_ast in args
                    ],
                )
            case ast.Attribute(value, attr):
                return js.ast.MemberExpression(
                    object=self.transform(value),
                    property=js.ast.Identifier(attr),
                )
            case ast.Name(id):
                return js.ast.Identifier(
                    name=id,
                )
            case ast.Constant(value):
                return js.ast.Literal(
                    value=value
                )
        raise Exception(f"Unmatched ast : {ast.dump(py_ast)}")
