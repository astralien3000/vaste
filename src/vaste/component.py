import inspect

import fastapi
import json

from vaste import js
from vaste import py
from vaste.vue.transformer.methods import MethodsTransformer
from vaste.vue.transformer.data import DataTransformer
from vaste.vue.transformer.render import RenderTransformer
from vaste.server_methods import ServerMethodsTransformer

from vaste.js.visitor.find_macro import FindMacroVisitor
from vaste.js.macro.macro import *

class VasteComponentJsMacro(JsMacro):

    def __init__(self, name, ast, api, macro_set = []):
        self.name = name
        self.ast = ast
        self.api = api
        self.macro_set = macro_set

    def unparse(self):
        return js.ast.unparse(
            js.ast.Program([
                *[
                    stmt
                    for macro in self.macro_set
                    for stmt in macro.import_list
                ],
                js.ast.ExportDefaultDeclaration(self.ast),
            ])
        )

    @property
    def filename(self):
        return f"./{self.name}.mjs"
    
    def save(self):
        for macro in self.macro_set:
            macro.save()
        with open(self.filename, "w") as file:
            file.write(self.unparse())

    def __repr__(self):
        return f"""VasteComponentJsMacro(name={self.name}, ast={self.ast})"""

    def match(self, path, py_ast):
        return py.ast.dump(py_ast) == py.ast.dump(path2ast(path))

    class Transformer(JsMacro.Transformer):

        def transform(self, _):
            return js.ast.Identifier(self.macro.name)

    @property
    def import_list(self):
        return [
            js.ast.ImportDeclaration(
                specifiers=[
                    js.ast.Identifier(self.name),
                ],
                source=js.ast.Literal(self.filename),
            ),
        ]


class SelfProxy:
    def __init__(self, data_dict: dict):
        self.data_dict = data_dict
    
    def __getattribute__(self, k: str):
        return object.__getattribute__(self, "data_dict").get(k, None)


def component(cls):
    frame = inspect.currentframe().f_back

    data_source = "if True:\n" + inspect.getsource(cls.data)
    data_py_ast = py.ast.parse(data_source)
    data_js_ast = DataTransformer().transform(data_py_ast)

    render_source = "if True:\n" + inspect.getsource(cls.render)
    render_py_ast = py.ast.parse(render_source)
    render_js_ast = RenderTransformer(frame).transform(render_py_ast)

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

    all_source = inspect.getsource(cls)
    all_py_ast = py.ast.parse(all_source)
    macro_set = FindMacroVisitor(frame).visit(all_py_ast)

    return VasteComponentJsMacro(
        name=cls.__name__,
        ast=js.ast.ObjectExpression([
            data_js_ast,
            methods_js_ast,
            render_js_ast,
        ]),
        api=api,
        macro_set=macro_set,
    )
