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
            case ast.Call(func, _, _):
                return ast.dump(func) == ast.dump(path2ast(path))
        return False

    def transform(self, parent, py_ast):
        match py_ast:
            case ast.Call(
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
                        js.ast.Literal(self.name),
                        js.ast.ObjectExpression([
                            self.transform(parent, kwarg)
                            for kwarg in kwargs
                            if kwarg.arg != "children"
                        ]),
                        js.ast.ArrayExpression([
                            parent.transform(elt)
                            for kwarg in kwargs
                            if kwarg.arg == "children"
                            for elt in kwarg.value.elts
                        ]),
                    ],
                )
            case ast.Call(
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
                        js.ast.Literal(self.name),
                        js.ast.ObjectExpression([
                            self.transform(parent, kwarg)
                            for kwarg in kwargs
                            if kwarg.arg != "children"
                        ]),
                        js.ast.ArrayExpression([
                            parent.transform(elt)
                            for elt in children_arg.elts
                        ]),
                    ],
                )
            case ast.keyword(arg, value):
                return js.ast.Property(
                    key=js.ast.Identifier(arg),
                    value=parent.transform(value)
                )
        # return parent.transform(py_ast)
        raise Exception(f"[VNodeJsMacro] Unmatched ast : {ast.dump(py_ast)}")
