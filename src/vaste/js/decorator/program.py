import inspect

from vaste.js.visitor.find_macro import FindMacroVisitor
from vaste.js.transformer.program import ProgramTransformer
from vaste import py

from vaste.js.macro.program import ProgramJsMacro


def program(cls):
    frame = inspect.currentframe().f_back
    tansformer = ProgramTransformer(frame)
    visitor = FindMacroVisitor(frame)

    cls_source = inspect.getsource(cls)
    try:
        cls_py_ast = py.ast.parse(cls_source)
    except IndentationError:
        cls_py_ast = py.ast.parse("if True:\n" + cls_source)

    match cls_py_ast:
        case py.ast.Module([py.ast.ClassDef(name, [], [], body)]):
            cls_js_ast = tansformer.transform(py.ast.Module(body))
            dep_list = visitor.visit(py.ast.Module(body))
            return ProgramJsMacro(name, cls_js_ast, dep_list)
        case py.ast.Module([py.ast.If(py.ast.Constant(True), [py.ast.ClassDef(name, [], [], body)])]):
            cls_js_ast = tansformer.transform(py.ast.Module(body))
            dep_list = visitor.visit(py.ast.Module(body))
            return ProgramJsMacro(name, cls_js_ast, dep_list)
    raise Exception(
        f"Unable to generate ProgramJsMacro from {py.ast.dump(cls_py_ast)}"
    )
