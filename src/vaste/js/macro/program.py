from .macro import *
from vaste import js
import os


class ProgramJsMacro(JsMacro):

    def __init__(self, name, ast, dependencies = []):
        self.name = name
        self.ast = ast
        self.dependencies = dependencies

    def unparse(self):
        return js.ast.unparse(
            js.ast.Program([
                *[
                    dep.gen_import_ast()
                    for dep in self.dependencies
                ],
                *self.ast.body,
            ])
        )

    @property
    def filename(self):
        return f"./{self.name}.mjs"
    
    def save(self):
        for dep in self.dependencies:
            dep.save()
        with open(self.filename, "w") as file:
            file.write(self.unparse())

    def exec(self):
        self.save()
        os.system(f"node {self.filename}")

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
        if k in ["name", "ast", "dependencies", *dir(ProgramJsMacro)]:
            return object.__getattribute__(self, k)
        return self

    def __call__(self, *args):
        return self

    def __repr__(self):
        return f"""ProgramJsMacro(name="{self.name}", ast={self.ast})"""

    def match(self, path, py_ast):
        return py.ast.dump(py_ast) == py.ast.dump(path2ast(path))

    class Transformer(JsMacro.Transformer):

        def transform(self, _):
            return js.ast.Identifier(self.macro.name)
