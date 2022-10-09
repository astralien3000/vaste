from vaste import js


class JsObjectRef:

    def __init__(self, ast):
        self.ast = ast

    def unparse(self):
        return object.__getattribute__(self, "ast").unparse()

    def __repr__(self):
        return f"""JsObjectRef(ast={
            repr(object.__getattribute__(self, "ast"))
        })"""

    def __getattribute__(self, k):
        return JsObjectRef(
            js.ast.MemberExpression(
                object.__getattribute__(self, "ast"),
                js.ast.Identifier(k),
            )
        )

    def __call__(self, *args):
        return JsObjectRef(
            js.ast.CallExpression(
                callee=object.__getattribute__(self, "ast"),
                arguments=[
                    js.ast.Literal(arg)
                    for arg in args
                ],
            )
        )


window = JsObjectRef(js.ast.Identifier("window"))
alert = JsObjectRef(js.ast.Identifier("alert"))
console = JsObjectRef(js.ast.Identifier("console"))
