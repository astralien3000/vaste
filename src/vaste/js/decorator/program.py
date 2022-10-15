import ast
import inspect

from vaste.js.transformer.default import DefaultTransformer
from vaste.js.transformer.macro import MacroTransformer
from vaste import js

from vaste.js.macro.macro import JsMacro


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


def map_py2js(module, path = []):
    return {
        **{
            (*path, k): getattr(module, k)
            for k in dir(module)
            if issubclass(type(getattr(module, k)), JsMacro)
        },
        **{
            mk: mv
            for k in dir(module)
            if inspect.ismodule(getattr(module, k))
            if k not in path
            for mk, mv in map_py2js(getattr(module, k), [*path, k]).items()
        },
    }


def program(cls):
    cls_source = inspect.getsource(cls)
    tansformer = MacroTransformer(
        map_py2js(inspect.getmodule(cls))
    )

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


# def fprogram(inject_ast):
#     def decorator(cls):
#         print(map_py2js(inspect.getmodule(cls)))
#         cls_source = inspect.getsource(cls)

#         try:
#             cls_py_ast = ast.parse(cls_source)
#         except IndentationError:
#             cls_py_ast = ast.parse("if True:\n" + cls_source)

#         match cls_py_ast:
#             case ast.Module([
#                 ast.ClassDef(
#                     name,
#                     [],
#                     [],
#                     body,
#                     [ast.Call(_, [ast.Name(inject_ast_name)])],
#                 )
#             ]):
#                 cls_js_ast = MacroTransformer(inject_ast, inject_ast_name).transform(ast.Module(body))
#                 return JsProgram(name, cls_js_ast)
#             case ast.Module([
#                 ast.If(
#                     ast.Constant(True),
#                     [ast.ClassDef(
#                         name,
#                         [],
#                         [],
#                         body,
#                         [ast.Call(_, [ast.Name(inject_ast_name)])]
#                     )]
#                 )
#             ]):
#                 cls_js_ast = MacroTransformer(inject_ast, inject_ast_name).transform(ast.Module(body))
#                 return JsProgram(name, cls_js_ast)
#         raise Exception(
#             f"Unable to generate JsProgram from {ast.dump(cls_py_ast)}"
#         )
#     return decorator
