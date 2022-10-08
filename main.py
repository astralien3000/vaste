import ast
import inspect


class js:

    class ast:

        def unparse(ast):
            return ast.unparse()

        class Program:
            def __init__(self, body: list = []):
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



def transform(py_ast, transform_cb=None):
    if transform_cb is None:
        transform_cb = transform
    match py_ast:
        case ast.Module(body):
            return js.ast.Program([
                transform_cb(stmt_ast)
                for stmt_ast in body
            ])
        case ast.Expr(value):
            return js.ast.ExpressionStatement(
                transform_cb(value)
            )
        case ast.Call(func, args):
            return js.ast.CallExpression(
                callee=transform_cb(func),
                arguments=[
                    transform_cb(expr_ast)
                    for expr_ast in args
                ],
            )
        case ast.Attribute(value, attr):
            return js.ast.MemberExpression(
                object=transform_cb(value),
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
                            value=v.vue_render_ast,
                        )
                        for k, v in self.props.items()
                    ]),
                    js.ast.ArrayExpression([
                        child.vue_render_ast
                        if hasattr(child, "vue_render_ast")
                        else js.ast.Literal(child)
                        for child in self.children
                    ]),
                ],
            )

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
        self.count = 0
        self.lool = "MIEW"

    class methods:

        def inc(self):
            self.count += 1

    def render(self):
        return button(
            children=[
                "My ", self.lool," count : ", self.count,
            ],
            onClick=self.inc,
        )


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

    class Helper:
        def __init__(self, k):
            self.k = k
        
        @property
        def vue_render_ast(self):
            return js.ast.MemberExpression(
                object=js.ast.Identifier("this"),
                property=js.ast.Identifier(self.k),
            )

    def __getattr__(self, k):
        return self.Helper(k)


def methods_transform(py_ast):
    match py_ast:
        case ast.Module([module_cls]):
            return methods_transform(module_cls)
        case ast.ClassDef("module", [], [], [methods_cls], []):
            return methods_transform(methods_cls)
        case ast.ClassDef("methods", [], [], body, []):
            return js.ast.Property(
                key=js.ast.Identifier("methods"),
                value=js.ast.ObjectExpression([
                    methods_transform(stmt)
                    for stmt in body
                ]),
            )
        case ast.FunctionDef(name, ast.arguments([], [ast.arg("self"), *args]), body, []):
            return js.ast.Property(
                key=js.ast.Identifier(name),
                value=js.ast.FunctionExpression(
                    params=[
                        methods_transform(arg)
                        for arg in args
                    ],
                    body=js.ast.BlockStatement([
                        methods_transform(stmt)
                        for stmt in body
                    ])
                ),
                method=True,
            )
        case ast.AugAssign(target, op, value):
            return js.ast.ExpressionStatement(
                js.ast.AssignmentExpression(
                    left=methods_transform(target),
                    operator=methods_transform(op)+"=",
                    right=methods_transform(value),
                ),
            )
        case ast.Add():
            return "+"
        case ast.Name("self"):
            return js.ast.Identifier(
                name="this",
            )
    return transform(py_ast, methods_transform)


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
    methods_js_ast = methods_transform(methods_py_ast)

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
print(
    js.ast.unparse(
        vue_prg_ast(
            js_component_ast(MyComponent)
        )
    )
)

@app.get("/", response_class=fastapi.responses.HTMLResponse)
def get_root():
    return f"""
        <html>
            <head>
                <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
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
