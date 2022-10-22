import ast


def path2ast(path):
    match path:
        case [name]:
            return ast.Name(name, ast.Load())
        case [*head, tail]:
            return ast.Attribute(path2ast(head), tail, ast.Load())


class JsMacro:

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
