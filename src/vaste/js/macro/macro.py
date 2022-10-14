import ast


def path2ast(path):
    match path:
        case [name]:
            return ast.Name(name, ast.Load())
        case [*head, tail]:
            return ast.Attribute(path2ast(head), tail, ast.Load())


class JsMacro:
    pass
