import ast
import inspect



class js:

    class ast:

        def unparse(ast):
            return ast.unparse()

        class Program:
            def __init__(self, body: list):
                self.body = body

            def unparse(self):
                return "".join([
                    stmt.unparse() for stmt in self.body
                ])

        class VariableDeclaration:
            def __init__(self, declarations: list, kind: str = "let"):
                self.declarations = declarations
                self.kind = kind

        class VariableDeclarator:
            def __init__(self, id, init):
                self.id = id
                self.init = init

        class Identifier:
            def __init__(self, name: str):
                self.name = name

            def unparse(self):
                return self.name

        class ArrayExpression:
            def __init__(self, elements: list):
                self.elements = elements

        class Literal:
            def __init__(self, value):
                self.value = value

            def unparse(self):
                match self.value:
                    case str():
                        return f'"{self.value}"'
                return str(self.value)

        class FunctionDeclaration:
            def __init__(self, id, body, params: list = []):
                self.id = id
                self.body = body
                self.params = params

        class BlockStatement:
            def __init__(self, body: list):
                self.body = body

            def unparse(self):
                return f"""{{{
                    "".join([
                        stmt.unparse() for stmt in self.body
                    ])
                }}}"""

        class ExpressionStatement:
            def __init__(self, expression):
                self.expression = expression

            def unparse(self):
                return f"{self.expression.unparse()};"

        class CallExpression:
            def __init__(self, callee, arguments: list):
                self.callee = callee
                self.arguments = arguments

            def unparse(self):
                return f"""{self.callee.unparse()}({",".join([
                    arg.unparse()
                    for arg in self.arguments
                ])})"""

        class MemberExpression:
            def __init__(self, object, property):
                self.object = object
                self.property = property

            def unparse(self):
                return f"{self.object.unparse()}.{self.property.unparse()}"

        class ArrowFunctionExpression:
            def __init__(self, body, params: list = []):
                self.body = body
                self.params = params

        class BinaryExpression:
            def __init__(self, left, operator: str, right):
                self.left = left
                self.operator = operator
                self.right = right

        class AssignmentExpression:
            def __init__(self, left, operator: str, right):
                self.left = left
                self.operator = operator
                self.right = right

            def unparse(self):
                return f"{self.left.unparse()}{self.operator}{self.right.unparse()}"

        class TemplateLiteral:
            def __init__(self, expressions: list, quasis: list):
                self.expressions = expressions
                self.quasis = quasis

        class TemplateElement:
            def __init__(self, value: str):
                self.value = value

        class ObjectExpression:
            def __init__(self, properties: list = []):
                self.properties = properties

            def unparse(self):
                return f"""{{{
                    ",".join([
                        prop.unparse()
                        for prop in self.properties
                    ])
                }}}"""

        class Property:
            def __init__(self, key: str, value, method: bool = False):
                self.key = key
                self.value = value
                self.method = method

            def unparse(self):
                if self.method:
                    return f"{self.key.unparse()}{self.value.unparse()}"
                else:
                    return f"{self.key.unparse()}:{self.value.unparse()}"

        class FunctionExpression:
            def __init__(self, body, params: list = []):
                self.body = body
                self.params = params

            def unparse(self):
                return f"""({
                    ",".join([
                        param.unparse()
                        for param in self.params
                    ])
                }){self.body.unparse()}"""

        class ReturnStatement:
            def __init__(self, argument):
                self.argument = argument

            def unparse(self):
                return f"return {self.argument.unparse()};"

        class ArrayExpression:
            def __init__(self, elements: list = []):
                self.elements = elements

            def unparse(self):
                return f"""[{
                    ",".join([
                        elem.unparse()
                        for elem in self.elements
                    ])
                }]"""



def transform(py_ast):
    match py_ast:
        case ast.Module(body):
            return js.ast.Program([
                transform(stmt_ast)
                for stmt_ast in body
            ])
        case ast.Expr(value):
            return js.ast.ExpressionStatement(
                transform(value)
            )
        case ast.Call(func, args):
            return js.ast.CallExpression(
                callee=transform(func),
                arguments=[
                    transform(expr_ast)
                    for expr_ast in args
                ],
            )
        case ast.Attribute(value, attr):
            return js.ast.MemberExpression(
                object=transform(value),
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


class JsModule:

    def __init__(self, py_ast):
        self.py_ast = py_ast
        self.js_ast = transform(py_ast)

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

class HtmlTag:
    def __init__(self, name):
        self.name = name
    
    class VNode:
        def __init__(self, type, props, children):
            self.type = type
            self.props = props
            self.children = children
        
        def __repr__(self):
            return f"""
                Vue.h(
                    "{self.type}",
                    {{ {", ".join([
                        f"{k}: {v}"
                        for k, v in self.props.items()
                    ])} }},
                    [ {",".join([
                        repr(child)
                        for child in self.children
                    ]) if self.children is not None else ""} ]
                )
            """

    def __call__(self, *args, **kwargs):
        match args:
            case []:
                return self.VNode(
                    type=self.name,
                    children=kwargs.get("children", None),
                    props={
                        k: v
                        for k, v in kwargs.items()
                        if k != "children"
                    },
                )
            case [children]:
                return self.VNode(
                    type=self.name,
                    children=children,
                    props=kwargs,
                )
        raise Exception("ERROR PARAM HtmlTag.__call__")

button = HtmlTag("button")
svg = HtmlTag("svg")
rect = HtmlTag("rect")


class MyComponent:

    def data(self):
        self.count = 1

    class methods:

        def inc(self):
            self.count += 1

    def render(self):
        # return button(
        #     children=[
        #         "count : ",
        #         self.count,
        #     ],
        #     on_click=self.inc,
        # )
        return svg(
            children=[
                rect(
                    x=0,
                    y=0,
                    width=100,
                    height=100,
                ),
            ],
        )


class DataProxy:

    def __init__(self):
        object.__setattr__(self, "data", {})

    def __setattr__(self, k, v):
        self.data[k] = v
    
    @property
    def vue_data_func(self):
        return f"""
            data() {{
                return {{
                    {",".join([
                        f"{k}: {v}"
                        for k, v in self.data.items()
                    ])}
                }};
            }}
        """


def test(cls):
    dp = DataProxy()
    cls.data(dp)
    print(dp.vue_data_func)
    render_res = cls.render(None)
    print(render_res)
    methods_source = "class module:\n" + inspect.getsource(cls.methods)
    print(methods_source)
    methods_py_ast = ast.parse(methods_source)
    print(ast.dump(methods_py_ast.body[0].body[0]))

test(MyComponent)

import fastapi

app = fastapi.FastAPI()


js_ast = js.ast.Program([
    js.ast.ExpressionStatement(
        js.ast.CallExpression(
            callee=js.ast.MemberExpression(
                object=js.ast.CallExpression(
                    callee=js.ast.MemberExpression(
                        object=js.ast.Identifier("Vue"),
                        property=js.ast.Identifier("createApp"),
                    ),
                    arguments=[
                        js.ast.ObjectExpression([
                            js.ast.Property(
                                key=js.ast.Identifier("data"),
                                value=js.ast.FunctionExpression(
                                    js.ast.BlockStatement([
                                        js.ast.ReturnStatement(
                                            js.ast.ObjectExpression([
                                                js.ast.Property(
                                                    key=js.ast.Identifier("count"),
                                                    value=js.ast.Literal(0),
                                                ),
                                            ]),
                                        ),
                                    ]),
                                ),
                                method=True,
                            ),
                            js.ast.Property(
                                key=js.ast.Identifier("methods"),
                                value=js.ast.ObjectExpression([
                                    js.ast.Property(
                                        key=js.ast.Identifier("inc"),
                                        value=js.ast.FunctionExpression(
                                            js.ast.BlockStatement([
                                                js.ast.ExpressionStatement(
                                                    js.ast.AssignmentExpression(
                                                        left=js.ast.MemberExpression(
                                                            object=js.ast.Identifier("this"),
                                                            property=js.ast.Identifier("count"),
                                                        ),
                                                        operator="+=",
                                                        right=js.ast.Literal(1),
                                                    ),
                                                ),
                                            ]),
                                        ),
                                        method=True,
                                    ),
                                ]),
                            ),
                            js.ast.Property(
                                key=js.ast.Identifier("render"),
                                value=js.ast.FunctionExpression(
                                    js.ast.BlockStatement([
                                        js.ast.ReturnStatement(
                                            js.ast.CallExpression(
                                                callee=js.ast.MemberExpression(
                                                    object=js.ast.Identifier("Vue"),
                                                    property=js.ast.Identifier("h"),
                                                ),
                                                arguments=[
                                                    js.ast.Literal("button"),
                                                    js.ast.ObjectExpression([
                                                        js.ast.Property(
                                                            key=js.ast.Identifier("onClick"),
                                                            value=js.ast.MemberExpression(
                                                                object=js.ast.Identifier("this"),
                                                                property=js.ast.Identifier("inc"),
                                                            ),
                                                        ),
                                                    ]),
                                                    js.ast.ArrayExpression([
                                                        js.ast.Literal("count : "),
                                                        js.ast.MemberExpression(
                                                            object=js.ast.Identifier("this"),
                                                            property=js.ast.Identifier("count"),
                                                        ),
                                                    ]),
                                                ],
                                            ),
                                        ),
                                    ]),
                                ),
                                method=True,
                            ),
                        ]),
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

print(js.ast.unparse(js_ast))


@app.get("/", response_class=fastapi.responses.HTMLResponse)
def get_root():
    return f"""
        <html>
            <head>
                <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
            </head>
            <body>
                <div id="app"></div>
                <script>{js.ast.unparse(js_ast)}</script>
            </body>
        </html>
    """
