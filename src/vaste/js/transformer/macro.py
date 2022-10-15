from operator import attrgetter
from .default import *

from vaste import js


class MacroTransformer(DefaultTransformer):

    def __init__(self, macro_map):
        self.macro_map = macro_map

    def transform(self, py_ast):
        for path, macro in self.macro_map.items():
            if type(macro).match(macro, path, py_ast):
                return type(macro).transform(macro, path, py_ast)
        # match py_ast:
        #     case ast.Attribute(value, attribute):
        #         print(value, attribute)
        #         pass
        #     # case ast.Call(ast.Name(self.inject_ast_name)):
        #     #     return self.inject_ast.pop()
        #     # case ast.Assign(
        #     #     [ast.Name(spec_name)],
        #     #     ast.Call(
        #     #         ast.Name("jsimport"),
        #     #         [ast.Constant(source)],
        #     #     ),
        #     # ):
        #     #     return js.ast.ImportDeclaration(
        #     #         specifiers=[
        #     #             js.ast.ImportNamespaceSpecifier(
        #     #                 js.ast.Identifier(spec_name),
        #     #             ),
        #     #         ],
        #     #         source=js.ast.Literal(source),
        #     #     )
        return DefaultTransformer.transform(self, py_ast)
