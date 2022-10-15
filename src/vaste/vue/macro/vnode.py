from vaste import js


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
                object=js.ast.Identifier("Vue"),
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


class VNodeFactory:
    def __init__(self, name):
        self.name = name

    def __call__(self, children = [], **kwargs):
        return VNode(
            type=self.name,
            children=children,
            props=kwargs,
        )
