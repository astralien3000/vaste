from .macro import *

from collections import deque


class InjectAstJsMacro(JsMacro):
    def __init__(self):
        self.data = deque()

    def __call__(self, arg):
        self.data.append(arg)
        return self
    
    def pop(self):
        return self.data.popleft()

    def match(self, path, py_ast):
        match py_ast:
            case ast.Call(func, args):
                return ast.dump(func) == ast.dump(path2ast(path))
        return False

    class Transformer(JsMacro.Transformer):

        def transform(self, _):
            return self.macro.pop()

    def __repr__(self):
        return "InjectAstJsMacro()"
