import ast
import inspect

from vaste import js

from vaste.js.transformer.default import DefaultTransformer
from vaste.js.transformer.methods import MethodsTransformer


class JsModule:

    def __init__(self, py_ast):
        self.py_ast = py_ast
        self.js_ast = DefaultTransformer().transform(py_ast)

    def code(self):
        # return ast.unparse(self.py_ast)
        return js.ast.unparse(self.js_ast)


def javascript(cls):
    cls_ast = ast.parse(
        inspect.getsource(cls),
        mode="exec",
    )
    return JsModule(ast.Module(cls_ast.body[0].body, []))


class JsObj:

    def __getattribute__(self, k):
        return self

    def __call__(self, *args, **kwds):
        return self


window = JsObj()
alert = JsObj()
console = JsObj()
Vue = JsObj()

@javascript
class MyJsModule:
    console.log("test")
    alert("LOOL")


def vnode_transform(vnode):
    if hasattr(vnode, "vue_render_ast"):
        return vnode.vue_render_ast
    else:
        return js.ast.Literal(vnode)


class HtmlTag:
    def __init__(self, name):
        self.name = name
    
    class VNode:
        def __init__(self, type, props, children):
            self.type = type
            self.props = props
            self.children = children
        
        @property
        def vue_render_ast(self):
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
                            value=vnode_transform(v),
                        )
                        for k, v in self.props.items()
                    ]),
                    js.ast.ArrayExpression([
                        vnode_transform(child)
                        for child in self.children
                    ]),
                ],
            )

    def __call__(self, children = [], **kwargs):
        return self.VNode(
            type=self.name,
            children=children,
            props=kwargs,
        )

button = HtmlTag("button")
svg = HtmlTag("svg")
rect = HtmlTag("rect")
div = HtmlTag("div")
nav = HtmlTag("nav")
a = HtmlTag("a")


class MyComponent:

    def data(self):
        self.count = 0
        self.lool = "MIEW"

    class methods:

        def inc(self):
            self.count += 10
        
        def reset(self):
            self.count = 0

    def render(self):
        return div([
            nav(
                Class="navbar navbar-primary bg-primary",
                children=[
                    a(
                        Class="navbar-brand",
                        href="#",
                        children="Title?",
                    ),
                ],
            ),
            div(
                children=[
                    button(
                        children=[
                            "My ", self.lool," count : ", self.count,
                        ],
                        onClick=self.inc,
                        Class="btn btn-primary",
                    ),
                    button(
                        children=["RESET"],
                        onClick=self.reset,
                        Class="btn btn-danger",
                    ),
                    svg(
                        children=[
                            rect(
                                x=0,
                                y=0,
                                width=100,
                                height=self.count + 50,
                            )
                        ],
                    ),
                ],
            ),
        ])


class DataProxy:

    def __init__(self):
        object.__setattr__(self, "data", {})

    def __setattr__(self, k, v):
        self.data[k] = v
    
    @property
    def vue_data_ast(self):
        return js.ast.Property(
            key=js.ast.Identifier("data"),
            value=js.ast.FunctionExpression(
                js.ast.BlockStatement([
                    js.ast.ReturnStatement(
                        js.ast.ObjectExpression([
                            js.ast.Property(
                                key=js.ast.Identifier(k),
                                value=js.ast.Literal(v),
                            )
                            for k, v in self.data.items()
                        ]),
                    ),
                ]),
            ),
            method=True,
        )


class RenderProxy:

    class MemberBOp:
        def __init__(self, member, operator, other):
            self.member = member
            self.operator = operator
            self.other = other
        
        @property
        def vue_render_ast(self):
            return js.ast.BinaryExpression(
                left=self.member.vue_render_ast,
                operator=self.operator,
                right=js.ast.Literal(self.other),
            )

    class Member:
        def __init__(self, k):
            self.k = k
        
        def __add__(self, other):
            return RenderProxy.MemberBOp(
                self, "+", other
            )

        @property
        def vue_render_ast(self):
            return js.ast.MemberExpression(
                object=js.ast.Identifier("this"),
                property=js.ast.Identifier(self.k),
            )

    def __getattr__(self, k):
        return RenderProxy.Member(k)


def js_component_ast(cls):
    dp = DataProxy()
    cls.data(dp)
    data_js_ast = dp.vue_data_ast

    rp = RenderProxy()
    render_res = cls.render(rp)
    render_js_ast = js.ast.Property(
        key=js.ast.Identifier("render"),
        value=js.ast.FunctionExpression(
            js.ast.BlockStatement([
                js.ast.ReturnStatement(
                    render_res.vue_render_ast
                ),
            ]),
        ),
        method=True,
    )

    methods_source = "class module:\n" + inspect.getsource(cls.methods)
    methods_py_ast = ast.parse(methods_source)
    methods_js_ast = MethodsTransformer().transform(methods_py_ast)

    return js.ast.ObjectExpression([
        data_js_ast,
        methods_js_ast,
        render_js_ast,
    ])


def vue_prg_ast(js_ast):
    return js.ast.Program([
        js.ast.ExpressionStatement(
            js.ast.CallExpression(
                callee=js.ast.MemberExpression(
                    object=js.ast.CallExpression(
                        callee=js.ast.MemberExpression(
                            object=js.ast.Identifier("Vue"),
                            property=js.ast.Identifier("createApp"),
                        ),
                        arguments=[
                            js_ast,
                        ],
                    ),
                    property=js.ast.Identifier("mount"),
                ),
                arguments=[
                    js.ast.Literal("#app"),
                ],
            )
        )
    ])

import fastapi

app = fastapi.FastAPI()


@app.get("/", response_class=fastapi.responses.HTMLResponse)
def get_root():
    return f"""
        <html>
            <head>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
                <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>
            </head>
            <body>
                <div id="app"></div>
                <script>{
                    js.ast.unparse(
                        vue_prg_ast(
                            js_component_ast(MyComponent)
                        )
                    )
                }</script>
            </body>
        </html>
    """
