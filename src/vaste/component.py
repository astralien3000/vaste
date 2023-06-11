import inspect

import fastapi
import json

from vaste import js
from vaste import py
from vaste.vue.transformer.methods import MethodsTransformer
from vaste.vue.transformer.data import DataTransformer
from vaste.vue.transformer.render import RenderTransformer
from vaste.server_methods import ServerMethodsTransformer


class VasteComponent:
    def __init__(self, name, ast, api):
        self.name = name
        self.ast = ast
        self.api = api

    def unparse(self):
        return js.ast.unparse(self.ast)

    def __repr__(self):
        return f"""VasteComponent(name={self.name}, ast={self.ast})"""


class SelfProxy:
    def __init__(self, data_dict: dict):
        self.data_dict = data_dict
    
    def __getattribute__(self, k: str):
        return object.__getattribute__(self, "data_dict").get(k, None)


def component(cls):
    data_source = "if True:\n" + inspect.getsource(cls.data)
    data_py_ast = py.ast.parse(data_source)
    data_js_ast = DataTransformer().transform(data_py_ast)

    render_source = "if True:\n" + inspect.getsource(cls.render)
    render_py_ast = py.ast.parse(render_source)
    render_js_ast = RenderTransformer(cls).transform(render_py_ast)

    if hasattr(cls, "methods"):
        methods_source = "class module:\n" + inspect.getsource(cls.methods)
        methods_py_ast = py.ast.parse(methods_source)
        methods_js_ast = MethodsTransformer().transform(methods_py_ast)
    else:
        methods_js_ast = js.ast.Property(
            key=js.ast.Identifier("methods"),
            method=False,
            value=js.ast.ObjectExpression([]),
        )

    api = fastapi.FastAPI()

    if hasattr(cls, "server_methods"):
        server_methods_source = "class module:\n" + inspect.getsource(cls.server_methods)
        server_methods_py_ast = py.ast.parse(server_methods_source)
        server_methods_js_ast = ServerMethodsTransformer().transform(server_methods_py_ast)

        methods_js_ast = js.ast.Property(
            key=js.ast.Identifier("methods"),
            method=False,
            value=js.ast.ObjectExpression([
                *methods_js_ast.value.properties,
                *server_methods_js_ast.value.properties,
            ]),
        )

        for attr in dir(cls.server_methods):
            if attr[0] != "_" and callable(getattr(cls.server_methods, attr)):
                method = getattr(cls.server_methods, attr)
                api.get(f"/{attr}")((lambda method: lambda self: {
                    "return": method(SelfProxy(json.loads(self)))
                })(method))

    return VasteComponent(
        name=cls.__name__,
        ast=js.ast.ObjectExpression([
            data_js_ast,
            methods_js_ast,
            render_js_ast,
        ]),
        api=api,
    )
