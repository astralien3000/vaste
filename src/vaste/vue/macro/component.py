from vaste import js
from vaste.js.macro.macro import *


class VueComponentJsMacro(JsMacro):

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
                    for stmt in macro.import_list
                ],
                js.ast.ExportDefaultDeclaration(self.ast),
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

    def __repr__(self):
        return f"""VueComponent(name={self.name}, ast={self.ast})"""

    def match(self, path, py_ast):
        return ast.dump(py_ast) == ast.dump(path2ast(path))

    class Transformer(JsMacro.Transformer):

        def transform(self, _):
            return js.ast.Identifier(self.macro.name)

    @property
    def import_list(self):
        return [
            js.ast.ImportDeclaration(
                specifiers=[
                    js.ast.Identifier(self.name),
                ],
                source=js.ast.Literal(self.filename),
            ),
        ]
