from vaste import js

from vaste.js.macro.macro import *
from vaste.js.transformer.default import DefaultTransformer


class VNode:

    def __init__(self, type, props, children):
        self.type = type
        self.props = props
        self.children = children

    @staticmethod
    def _transform(vnode):
        if hasattr(vnode, "ast"):
            return vnode.ast
        else:
            return js.ast.Literal(vnode)

    @property
    def ast(self):
        return js.ast.CallExpression(
            callee=js.ast.MemberExpression(
                object=js.ast.Identifier("vue"),
                property=js.ast.Identifier("h"),
            ),
            arguments=[
                js.ast.Literal(self.type),
                js.ast.ObjectExpression([
                    js.ast.Property(
                        key=js.ast.Identifier(k),
                        value=self._transform(v),
                    )
                    for k, v in self.props.items()
                ]),
                js.ast.ArrayExpression([
                    self._transform(child)
                    for child in self.children
                ]),
            ],
        )


class VNodeJsMacro(JsMacro):
    def __init__(self, name):
        self.name = name

    def __call__(self, children = [], **kwargs):
        return VNode(
            type=self.name,
            children=children,
            props=kwargs,
        )

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
