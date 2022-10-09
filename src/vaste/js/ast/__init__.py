

def unparse(ast):
    return ast.unparse()


class Program:
    def __init__(self, body: list = []):
        self.body = body

    def unparse(self):
        return "".join([
            stmt.unparse() for stmt in self.body
        ])

    def __repr__(self):
        return f"""Program(body={self.body})"""


class VariableDeclaration:
    def __init__(self, declarations: list, kind: str = "let"):
        self.declarations = declarations
        self.kind = kind


class VariableDeclarator:
    def __init__(self, id, init):
        self.id = id
        self.init = init


class Identifier:
    def __init__(self, name: str):
        self.name = name

    def unparse(self):
        return self.name

    def __repr__(self):
        return f"""Identifier(name="{self.name}")"""


class ArrayExpression:
    def __init__(self, elements: list):
        self.elements = elements


class Literal:
    def __init__(self, value):
        self.value = value

    def unparse(self):
        match self.value:
            case str():
                return f'"{self.value}"'
        return str(self.value)

    def __repr__(self):
        match self.value:
            case str():
                return f"""Literal(value="{self.value}")"""
        return f"""Literal(value={self.value})"""


class FunctionDeclaration:
    def __init__(self, id, body, params: list = []):
        self.id = id
        self.body = body
        self.params = params


class BlockStatement:
    def __init__(self, body: list):
        self.body = body

    def unparse(self):
        return f"""{{{
            "".join([
                stmt.unparse() for stmt in self.body
            ])
        }}}"""


class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression

    def unparse(self):
        return f"{self.expression.unparse()};"

    def __repr__(self):
        return f"""ExpressionStatement(expression={self.expression})"""


class CallExpression:
    def __init__(self, callee, arguments: list):
        self.callee = callee
        self.arguments = arguments

    def unparse(self):
        return f"""{self.callee.unparse()}({",".join([
            arg.unparse()
            for arg in self.arguments
        ])})"""

    def __repr__(self):
        return f"""CallExpression({
            ", ".join([
                f"callee={self.callee}",
                f"arguments={self.arguments}",
            ])
        })"""


class MemberExpression:
    def __init__(self, object, property):
        self.object = object
        self.property = property

    def unparse(self):
        return f"{self.object.unparse()}.{self.property.unparse()}"

    def __repr__(self):
        return f"""CallExpression({
            ", ".join([
                f"object={self.object}",
                f"property={self.property}",
            ])
        })"""


class ArrowFunctionExpression:
    def __init__(self, body, params: list = []):
        self.body = body
        self.params = params


class BinaryExpression:
    def __init__(self, left, operator: str, right):
        self.left = left
        self.operator = operator
        self.right = right

    def unparse(self):
        return f"{self.left.unparse()}{self.operator}{self.right.unparse()}"


class AssignmentExpression:
    def __init__(self, left, operator: str, right):
        self.left = left
        self.operator = operator
        self.right = right

    def unparse(self):
        return f"{self.left.unparse()}{self.operator}{self.right.unparse()}"


class TemplateLiteral:
    def __init__(self, expressions: list, quasis: list):
        self.expressions = expressions
        self.quasis = quasis


class TemplateElement:
    def __init__(self, value: str):
        self.value = value


class ObjectExpression:
    def __init__(self, properties: list = []):
        self.properties = properties

    def unparse(self):
        return f"""{{{
            ",".join([
                prop.unparse()
                for prop in self.properties
            ])
        }}}"""


class Property:
    def __init__(self, key: str, value, method: bool = False):
        self.key = key
        self.value = value
        self.method = method

    def unparse(self):
        if self.method:
            return f"{self.key.unparse()}{self.value.unparse()}"
        else:
            return f"{self.key.unparse()}:{self.value.unparse()}"


class FunctionExpression:
    def __init__(self, body, params: list = []):
        self.body = body
        self.params = params

    def unparse(self):
        return f"""({
            ",".join([
                param.unparse()
                for param in self.params
            ])
        }){self.body.unparse()}"""


class ReturnStatement:
    def __init__(self, argument):
        self.argument = argument

    def unparse(self):
        return f"return {self.argument.unparse()};"


class ArrayExpression:
    def __init__(self, elements: list = []):
        self.elements = elements

    def unparse(self):
        return f"""[{
            ",".join([
                elem.unparse()
                for elem in self.elements
            ])
        }]"""
