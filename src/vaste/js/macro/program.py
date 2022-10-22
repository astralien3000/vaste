from .macro import *
from vaste import js
import os


class ProgramJsMacro(JsMacro):

    def __init__(self, name, ast, macro_set = []):
        self.name = name
        self.ast = ast
        self.macro_set = macro_set

    def unparse(self):
        return js.ast.unparse(
            js.ast.Program([
                *[
                    stmt
                    for macro in self.macro_set
                    for stmt in (macro.import_list, print(macro))[0]
                ],
                *self.ast.body,
            ])
        )

    @property
    def filename(self):
        return f"./{self.name}.mjs"
    
    def save(self):
        for macro in self.macro_set:
            macro.save()
        with open(self.filename, "w") as file:
            file.write(self.unparse())

    def exec(self):
        self.save()
        os.system(f"node {self.filename}")

    @property
    def import_list(self):
        return [
            js.ast.ImportDeclaration(
                specifiers=[
                    js.ast.ImportNamespaceSpecifier(
                        js.ast.Identifier(self.name)
                    ),
                ],
                source=js.ast.Literal(self.filename),
            ),
        ]

    def __getattribute__(self, k):
        if k in ["name", "ast", "macro_set", *dir(ProgramJsMacro)]:
            return object.__getattribute__(self, k)
        return self

    def __call__(self, *args):
        return self

    def __repr__(self):
        return f"""ProgramJsMacro(name="{self.name}", ast={self.ast})"""

    def match(self, path, py_ast):
        return ast.dump(py_ast) == ast.dump(path2ast(path))

    class Transformer(JsMacro.Transformer):

        def transform(self, _):
            return js.ast.Identifier(self.macro.name)
