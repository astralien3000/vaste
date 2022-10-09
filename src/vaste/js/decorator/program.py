import ast
import inspect

from vaste.js.transformer.default import DefaultTransformer
from vaste import js


class JsProgram:

    def __init__(self, name, ast):
        self.name = name
        self.ast = ast

    def unparse(self):
        return js.ast.unparse(self.ast)
    
    def __repr__(self):
        return f"""JsProgram(name="{self.name}", ast={
            self.ast
        })"""


def program(cls):
    cls_source = inspect.getsource(cls)
    cls_py_ast = ast.parse(cls_source)
    match cls_py_ast:
        case ast.Module([ast.ClassDef(name, [], [], body)]):
            cls_js_ast = DefaultTransformer().transform(ast.Module(body))
            return JsProgram(name, cls_js_ast)
    raise Exception(
        f"Unable to generate JsProgram from {ast.dump(cls_py_ast)}"
    )
