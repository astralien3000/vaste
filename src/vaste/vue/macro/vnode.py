from vaste import js

from vaste.js.macro.macro import *


class VNodeJsMacro(JsMacro):
    def __init__(self, name):
        self.name = name

    def match(self, path, py_ast):
        match py_ast:
            case py.ast.Call(func, _, _):
                return py.ast.dump(func) == py.ast.dump(path2ast(path))
        return False

    class Transformer(JsMacro.Transformer):

        def transform(self, py_ast):
            match py_ast:
                case py.ast.Call(
                    _,
                    [],
                    kwargs,
                ):
                    return js.ast.CallExpression(
                        callee=js.ast.MemberExpression(
                            object=js.ast.Identifier("vue"),
                            property=js.ast.Identifier("h"),
                        ),
                        arguments=[
                            js.ast.Literal(self.macro.name),
                            js.ast.ObjectExpression([
                                self.transform(kwarg)
                                for kwarg in kwargs
                                if kwarg.arg != "children"
                            ]),
                            *[
                                self.parent.transform(kwarg.value)
                                for kwarg in kwargs
                                if kwarg.arg == "children"
                            ],
                        ],
                    )
                case py.ast.Call(
                    _,
                    [children_arg],
                    kwargs,
                ):
                    return js.ast.CallExpression(
                        callee=js.ast.MemberExpression(
                            object=js.ast.Identifier("vue"),
                            property=js.ast.Identifier("h"),
                        ),
                        arguments=[
                            js.ast.Literal(self.macro.name),
                            js.ast.ObjectExpression([
                                self.transform(kwarg)
                                for kwarg in kwargs
                                if kwarg.arg != "children"
                            ]),
                            js.ast.ArrayExpression([
                                self.parent.transform(elt)
                                for elt in children_arg.elts
                            ]),
                        ],
                    )
                case py.ast.keyword(arg, value):
                    return js.ast.Property(
                        key=js.ast.Identifier(arg),
                        value=self.parent.transform(value)
                    )
            raise Exception(f"[VNodeJsMacro] Unmatched ast : {py.ast.dump(py_ast)}")
