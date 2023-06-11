from vaste import py


def path2ast(path):
    match path:
        case [name]:
            return py.ast.Name(name, py.ast.Load())
        case [*head, tail]:
            return py.ast.Attribute(path2ast(head), tail, py.ast.Load())


class JsMacro:

    def __call__(self, *_):
        return self
    
    def save(self):
        pass

    def match(self, path, py_ast):
        return py.ast.dump(py_ast) == py.ast.dump(path2ast(path))

    class Transformer:
        
        def __init__(self, macro, parent, path):
            self.macro = macro
            self.parent = parent
            self.path = path

        def transform(self, _):
            raise Exception(f"{type(self.macro)} transform : Not Implemented")

    def transformer(self, parent, path):
        return type(self).Transformer(
            macro=self,
            parent=parent,
            path=path,
        )

    @property
    def import_list(self):
        return []
