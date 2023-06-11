import inspect

from vaste import js
from vaste import py
from vaste.vue.transformer.methods import MethodsTransformer
from vaste.vue.transformer.data import DataTransformer
from vaste.vue.transformer.render import RenderTransformer


class VueComponent:
    def __init__(self, name, ast):
        self.name = name
        self.ast = ast

    def unparse(self):
        return js.ast.unparse(self.ast)

    def __repr__(self):
        return f"""VueComponent(name={self.name}, ast={self.ast})"""


# class DataProxy:

#     def __init__(self):
#         object.__setattr__(self, "data", {})

#     def __setattr__(self, k, v):
#         self.data[k] = v
    
#     @property
#     def vue_data_ast(self):
#         return js.ast.Property(
#             key=js.ast.Identifier("data"),
#             value=js.ast.FunctionExpression(
#                 js.ast.BlockStatement([
#                     js.ast.ReturnStatement(
#                         js.ast.ObjectExpression([
#                             js.ast.Property(
#                                 key=js.ast.Identifier(k),
#                                 value=js.ast.Literal(v),
#                             )
#                             for k, v in self.data.items()
#                         ]),
#                     ),
#                 ]),
#             ),
#             method=True,
#         )


# class RenderProxy:

#     class MemberBOp:
#         def __init__(self, member, operator, other):
#             self.member = member
#             self.operator = operator
#             self.other = other
        
#         @property
#         def ast(self):
#             return js.ast.BinaryExpression(
#                 left=self.member.ast,
#                 operator=self.operator,
#                 right=js.ast.Literal(self.other),
#             )

#     class Member:
#         def __init__(self, k):
#             self.k = k
        
#         def __add__(self, other):
#             return RenderProxy.MemberBOp(
#                 self, "+", other
#             )

#         @property
#         def ast(self):
#             return js.ast.MemberExpression(
#                 object=js.ast.Identifier("this"),
#                 property=js.ast.Identifier(self.k),
#             )

#     def __getattr__(self, k):
#         return RenderProxy.Member(k)


def component(cls):
    # dp = DataProxy()
    # cls.data(dp)
    # data_js_ast = dp.vue_data_ast

    data_source = "if True:\n" + inspect.getsource(cls.data)
    data_py_ast = py.ast.parse(data_source)
    data_js_ast = DataTransformer().transform(data_py_ast)

    # old_rp = RenderProxy()
    # old_render_res = cls.render(old_rp)
    # old_render_js_ast = js.ast.Property(
    #     key=js.ast.Identifier("render"),
    #     value=js.ast.FunctionExpression(
    #         js.ast.BlockStatement([
    #             js.ast.ReturnStatement(
    #                 old_render_res.ast
    #             ),
    #         ]),
    #     ),
    #     method=True,
    # )

    render_source = "if True:\n" + inspect.getsource(cls.render)
    render_py_ast = py.ast.parse(render_source)
    render_js_ast = RenderTransformer(cls).transform(render_py_ast)

    methods_source = "class module:\n" + inspect.getsource(cls.methods)
    methods_py_ast = py.ast.parse(methods_source)
    methods_js_ast = MethodsTransformer().transform(methods_py_ast)

    return VueComponent(
        cls.__name__,
        js.ast.ObjectExpression([
            data_js_ast,
            methods_js_ast,
            # old_render_js_ast,
            render_js_ast,
        ])
    )
