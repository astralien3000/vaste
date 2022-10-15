from .macro import *
from vaste import js


class ProgramJsMacro(JsMacro):

    def __init__(self, name, ast):
        self.name = name
        self.ast = ast

    def unparse(self):
        return js.ast.unparse(self.ast)

    @property
    def filename(self):
        return f"./{self.name}.mjs"

    def gen_import_ast(self):
        return js.ast.ImportDeclaration(
            specifiers=[
                js.ast.ImportNamespaceSpecifier(
                    js.ast.Identifier(self.name)
                ),
            ],
            source=js.ast.Literal(self.filename),
        )

    def __getattribute__(self, k):
        if k in ["name", "ast", *dir(ProgramJsMacro)]:
            return object.__getattribute__(self, k)
        return self

    def __repr__(self):
        return f"""ProgramJsMacro(name="{self.name}", ast={self.ast})"""

    def match(self, path, py_ast):
        return ast.dump(py_ast) == ast.dump(path2ast(path))

    class Transformer(JsMacro.Transformer):

        def transform(self, _):
            return js.ast.Identifier(self.macro.name)
