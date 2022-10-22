import ast
import inspect

from vaste.js.visitor.find_macro import FindMacroVisitor
from vaste.js.transformer.program import ProgramTransformer
from vaste import js

from vaste.js.macro.program import ProgramJsMacro


def program(cls):
    frame = inspect.currentframe().f_back
    tansformer = ProgramTransformer(frame)
    visitor = FindMacroVisitor(frame)

    cls_source = inspect.getsource(cls)
    try:
        cls_py_ast = ast.parse(cls_source)
    except IndentationError:
        cls_py_ast = ast.parse("if True:\n" + cls_source)

    match cls_py_ast:
        case ast.Module([ast.ClassDef(name, [], [], body)]):
            cls_js_ast = tansformer.transform(ast.Module(body))
            macro_set = visitor.visit(ast.Module(body))
            return ProgramJsMacro(name, cls_js_ast, macro_set)
        case ast.Module([ast.If(ast.Constant(True), [ast.ClassDef(name, [], [], body)])]):
            cls_js_ast = tansformer.transform(ast.Module(body))
            macro_set = visitor.visit(ast.Module(body))
            return ProgramJsMacro(name, cls_js_ast, macro_set)
    raise Exception(
        f"Unable to generate ProgramJsMacro from {ast.dump(cls_py_ast)}"
    )
