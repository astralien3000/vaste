from .macro import *
from vaste import js
from vaste import py


class AttributeJsMacro(JsMacro):

    def __init__(self, object_macro, key):
        self.object_macro = object_macro
        self.key = key

    class Transformer(JsMacro.Transformer):

        def transform(self, py_ast):
            sub_transformer = self.macro.object_macro.transformer(self.parent, self.path)
            return js.ast.MemberExpression(
                object=sub_transformer.transform(py_ast),
                property=js.ast.Identifier(self.macro.key),
            )
        
    def save(self):
        return self.object_macro.save()

    @property
    def import_list(self):
        return self.object_macro.import_list


class ObjectJsMacro(JsMacro):

    def __init__(self, name):
        self.name = name

    def __getattribute__(self, k):
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            return AttributeJsMacro(self, k)

    def match(self, path, py_ast):
        return py.ast.dump(py_ast) == py.ast.dump(path2ast(path))

    class Transformer(JsMacro.Transformer):

        def transform(self, _):
            return js.ast.Identifier(self.macro.name)

    def __repr__(self):
        return f"""ObjectJsMacro(name={
            repr(self.name)
        })"""
