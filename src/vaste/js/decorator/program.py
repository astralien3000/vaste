import ast
import inspect

from vaste.js.transformer.default import DefaultTransformer
from vaste.js.transformer.unquote import UnquoteTransformer
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


def program(cls, tansformer = DefaultTransformer()):
    cls_source = inspect.getsource(cls)

    try:
        cls_py_ast = ast.parse(cls_source)
    except IndentationError:
        cls_py_ast = ast.parse("if True:\n" + cls_source)

    match cls_py_ast:
        case ast.Module([ast.ClassDef(name, [], [], body)]):
            cls_js_ast = tansformer.transform(ast.Module(body))
            return JsProgram(name, cls_js_ast)
        case ast.Module([ast.If(ast.Constant(True), [ast.ClassDef(name, [], [], body)])]):
            cls_js_ast = tansformer.transform(ast.Module(body))
            return JsProgram(name, cls_js_ast)
    raise Exception(
        f"Unable to generate JsProgram from {ast.dump(cls_py_ast)}"
    )


def fprogram(unquote):
    def decorator(cls):
        cls_source = inspect.getsource(cls)

        try:
            cls_py_ast = ast.parse(cls_source)
        except IndentationError:
            cls_py_ast = ast.parse("if True:\n" + cls_source)

        match cls_py_ast:
            case ast.Module([ast.ClassDef(name, [], [], body, [ast.Call(_, [ast.Name(unquote_name)])])]):
                cls_js_ast = UnquoteTransformer(unquote, unquote_name).transform(ast.Module(body))
                return JsProgram(name, cls_js_ast)
            case ast.Module([ast.If(ast.Constant(True), [ast.ClassDef(name, [], [], body, [ast.Call(_, [ast.Name(unquote_name)])])])]):
                cls_js_ast = UnquoteTransformer(unquote, unquote_name).transform(ast.Module(body))
                return JsProgram(name, cls_js_ast)
        raise Exception(
            f"Unable to generate JsProgram from {ast.dump(cls_py_ast)}"
        )
    return decorator

    return lambda cls: program(
        cls, UnquoteTransformer(unquote)
    )
