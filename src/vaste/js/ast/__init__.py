

from types import NoneType
from dataclasses import dataclass, field


def unparse(ast):
    return ast.unparse()


class AST:
    """
    Base of all AST node classes.
    Mainly used for type hints.
    """


@dataclass
class Program(AST):
    body: list[AST] = field(default_factory=list)

    def unparse(self):
        return "".join([
            stmt.unparse() for stmt in self.body
        ])


@dataclass
class VariableDeclaration(AST):
    declarations: list[AST]
    kind: str = "let"

    def unparse(self):
        return f"""{self.kind} {
            ",".join([
                vdecl.unparse()
                for vdecl in self.declarations
            ])
        };"""


@dataclass
class ExportNamedDeclaration(AST):
    declarations: list[AST]

    def unparse(self):
        return f"""export {
            ",".join([
                vdecl.unparse()
                for vdecl in self.declarations
            ])
        };"""


@dataclass
class ExportDefaultDeclaration(AST):
    declaration: list[AST]

    def unparse(self):
        return f"""export default {
            self.declaration.unparse()
        };"""


@dataclass
class VariableDeclarator(AST):
    id: AST
    init: AST

    def unparse(self):
        return f"""{self.id.unparse()}={self.init.unparse()}"""


@dataclass
class Identifier(AST):
    name: str

    def unparse(self):
        return self.name


@dataclass
class ArrayExpression(AST):
    elements: list[AST]


@dataclass
class Literal(AST):
    value: str|bool|float|NoneType

    def unparse(self):
        match self.value:
            case NoneType():
                return "null"
            case str():
                return f'"{self.value}"'
            case bool():
                return "true" if self.value else "false"
        return str(self.value)


@dataclass
class FunctionDeclaration(AST):
    id: AST
    body: AST
    params: list[AST] = field(default_factory=list)

    def unparse(self):
        return f"""function {self.id.unparse()}({
            ",".join([
                param.unparse()
                for param in self.params
            ])
        }){self.body.unparse()};"""


@dataclass
class BlockStatement(AST):
    body: list[AST]

    def unparse(self):
        return f"""{{{
            "".join([
                stmt.unparse() for stmt in self.body
            ])
        }}}"""


@dataclass
class ExpressionStatement(AST):
    expression: AST

    def unparse(self):
        return f"{self.expression.unparse()};"


@dataclass
class CallExpression(AST):
    callee: AST
    arguments: list[AST]

    def unparse(self):
        return f"""{self.callee.unparse()}({",".join([
            arg.unparse()
            for arg in self.arguments
        ])})"""


@dataclass
class NewExpression(AST):
    callee: AST
    arguments: list[AST]

    def unparse(self):
        return f"""new {self.callee.unparse()}({",".join([
            arg.unparse()
            for arg in self.arguments
        ])})"""


@dataclass
class MemberExpression(AST):
    object: AST
    property: AST
    computed: bool = False

    def unparse(self):
        if self.computed:
            return f"{self.object.unparse()}[{self.property.unparse()}]"
        return f"{self.object.unparse()}.{self.property.unparse()}"


@dataclass
class ArrowFunctionExpression(AST):
    body: AST
    params: list[AST] = field(default_factory=list)

    def unparse(self):
        return f"""({
            ",".join([
                param.unparse()
                for param in self.params
            ])
        })=>{self.body.unparse()}"""


@dataclass
class BinaryExpression(AST):
    left: AST
    operator: str
    right: AST

    def unparse(self):
        return f"{self.left.unparse()}{self.operator}{self.right.unparse()}"


@dataclass
class AssignmentExpression(AST):
    left: AST
    operator: str
    right: AST

    def unparse(self):
        return f"{self.left.unparse()}{self.operator}{self.right.unparse()}"


@dataclass
class TemplateLiteral(AST):
    expressions: list[AST]
    quasis: list[AST]


@dataclass
class TemplateElement(AST):
    value: str


@dataclass
class ObjectExpression(AST):
    properties: list[AST] = field(default_factory=list)

    def unparse(self):
        return f"""{{{
            ",".join([
                prop.unparse()
                for prop in self.properties
            ])
        }}}"""


@dataclass
class Property(AST):
    key: str
    value: AST
    method: bool = False

    def unparse(self):
        if self.method:
            return f"{self.key.unparse()}{self.value.unparse()}"
        else:
            return f"{self.key.unparse()}:{self.value.unparse()}"


@dataclass
class FunctionExpression(AST):
    body: AST
    params: list[AST] = field(default_factory=list)

    def unparse(self):
        return f"""({
            ",".join([
                param.unparse()
                for param in self.params
            ])
        }){self.body.unparse()}"""


@dataclass
class ReturnStatement(AST):
    argument: AST

    def unparse(self):
        return f"return {self.argument.unparse()};"


@dataclass
class ArrayExpression(AST):
    elements: list[AST] = field(default_factory=list)

    def unparse(self):
        return f"""[{
            ",".join([
                elem.unparse()
                for elem in self.elements
            ])
        }]"""


@dataclass
class ImportDeclaration(AST):
    specifiers: list[AST]
    source: AST

    def unparse(self):
        if len(self.specifiers) == 0:
            return f"""import {
                self.source.unparse()
            };"""
        return f"""import {
            ",".join([
                spec.unparse()
                for spec in self.specifiers
            ])
        } from {
            self.source.unparse()
        };"""


@dataclass
class ImportNamespaceSpecifier(AST):
    local: AST

    def unparse(self):
        return f"""* as {
            self.local.unparse()
        }"""
