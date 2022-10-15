import ast
import inspect

from vaste.js.visitor.dependency import DependencyVisitor
from vaste.js.transformer.program import ProgramTransformer
from vaste import js

from vaste.js.macro.program import ProgramJsMacro


def program(cls):
    cls_source = inspect.getsource(cls)
    tansformer = ProgramTransformer(cls)
    visitor = DependencyVisitor(cls)

    try:
        cls_py_ast = ast.parse(cls_source)
    except IndentationError:
        cls_py_ast = ast.parse("if True:\n" + cls_source)

    match cls_py_ast:
        case ast.Module([ast.ClassDef(name, [], [], body)]):
            cls_js_ast = tansformer.transform(ast.Module(body))
            dep_list = visitor.visit(ast.Module(body))
            cls_js_ast.body = [
                *[
                    dep.gen_import_ast()
                    for dep in dep_list
                ],
                *cls_js_ast.body
            ]
            return ProgramJsMacro(name, cls_js_ast)
        case ast.Module([ast.If(ast.Constant(True), [ast.ClassDef(name, [], [], body)])]):
            cls_js_ast = tansformer.transform(ast.Module(body))
            dep_list = visitor.visit(ast.Module(body))
            cls_js_ast.body = [
                *[
                    dep.gen_import_ast()
                    for dep in dep_list
                ],
                *cls_js_ast.body
            ]
            return ProgramJsMacro(name, cls_js_ast)
    raise Exception(
        f"Unable to generate ProgramJsMacro from {ast.dump(cls_py_ast)}"
    )
