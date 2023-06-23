import inspect

from vaste import js
from vaste import py
from vaste.vue.transpiler.methods import MethodsTranspiler
from vaste.vue.transpiler.data import DataTranspiler
from vaste.vue.transpiler.render import RenderTranspiler

from vaste.js.visitor.find_macro import FindMacroVisitor

from vaste.vue.macro.component import VueComponentJsMacro


def component(cls):
    frame = inspect.currentframe().f_back

    data_source = "if True:\n" + inspect.getsource(cls.data)
    data_py_ast = py.ast.parse(data_source)
    data_js_ast = DataTranspiler().transpile(data_py_ast)

    render_source = "if True:\n" + inspect.getsource(cls.render)
    render_py_ast = py.ast.parse(render_source)
    render_js_ast = RenderTranspiler(frame).transpile(render_py_ast)

    methods_source = "class module:\n" + inspect.getsource(cls.methods)
    methods_py_ast = py.ast.parse(methods_source)
    methods_js_ast = MethodsTranspiler().transpile(methods_py_ast)

    all_source = inspect.getsource(cls)
    all_py_ast = py.ast.parse(all_source)
    macro_set = FindMacroVisitor(frame).visit(all_py_ast)

    return VueComponentJsMacro(
        cls.__name__,
        js.ast.ObjectExpression(
            [
                data_js_ast,
                methods_js_ast,
                render_js_ast,
            ]
        ),
        macro_set,
    )
