from .macro import *
from vaste import js


class ImportFromJsMacro(JsMacro):

    class Helper:

        def __getattribute__(self, k):
            return self

        def __call__(self, *args):
            return self

    def __call__(self, arg):
        return self.Helper()

    def match(self, path, py_ast):
        match py_ast:
            case ast.Assign(_, ast.Call(func, _)):
                return ast.dump(func) == ast.dump(path2ast(path))
        return False

    class Transformer(JsMacro.Transformer):

        def transform(self, py_ast):
            match py_ast:
                case ast.Assign(
                    [ast.Name(spec_name)],
                    ast.Call(
                        _,
                        [ast.Constant(source)],
                    ),
                ):
                    return js.ast.ImportDeclaration(
                        specifiers=[
                            js.ast.ImportNamespaceSpecifier(
                                js.ast.Identifier(spec_name),
                            ),
                        ],
                        source=js.ast.Literal(source),
                    )
            raise Exception("ERROR in ImportJsMacro.transform")

    def __repr__(self):
        return "ImportJsMacro()"
