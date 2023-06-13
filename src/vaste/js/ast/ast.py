from types import NoneType as _NoneType
from dataclasses import (
    dataclass as _dataclass,
    field as _field,
)


class AST:
    """
    Base of all AST node classes.
    Mainly used for type hints.
    """


@_dataclass
class Program(AST):
    body: list[AST] = _field(default_factory=list)


@_dataclass
class VariableDeclaration(AST):
    declarations: list[AST]
    kind: str = "let"


@_dataclass
class ExportNamedDeclaration(AST):
    declarations: list[AST]


@_dataclass
class ExportDefaultDeclaration(AST):
    declaration: list[AST]


@_dataclass
class VariableDeclarator(AST):
    id: AST
    init: AST


@_dataclass
class Identifier(AST):
    name: str


@_dataclass
class ArrayExpression(AST):
    elements: list[AST]


@_dataclass
class Literal(AST):
    value: str|bool|float|_NoneType


@_dataclass
class FunctionDeclaration(AST):
    id: AST
    body: AST
    params: list[AST] = _field(default_factory=list)


@_dataclass
class BlockStatement(AST):
    body: list[AST]


@_dataclass
class ExpressionStatement(AST):
    expression: AST


@_dataclass
class CallExpression(AST):
    callee: AST
    arguments: list[AST]


@_dataclass
class NewExpression(AST):
    callee: AST
    arguments: list[AST]


@_dataclass
class MemberExpression(AST):
    object: AST
    property: AST
    computed: bool = False


@_dataclass
class ArrowFunctionExpression(AST):
    body: AST
    params: list[AST] = _field(default_factory=list)


@_dataclass
class BinaryExpression(AST):
    left: AST
    operator: str
    right: AST


@_dataclass
class AssignmentExpression(AST):
    left: AST
    operator: str
    right: AST


@_dataclass
class TemplateLiteral(AST):
    expressions: list[AST]
    quasis: list[AST]


@_dataclass
class TemplateElement(AST):
    value: str


@_dataclass
class ObjectExpression(AST):
    properties: list[AST] = _field(default_factory=list)


@_dataclass
class Property(AST):
    key: str
    value: AST
    method: bool = False


@_dataclass
class FunctionExpression(AST):
    body: AST
    params: list[AST] = _field(default_factory=list)


@_dataclass
class ReturnStatement(AST):
    argument: AST


@_dataclass
class ArrayExpression(AST):
    elements: list[AST] = _field(default_factory=list)


@_dataclass
class ImportDeclaration(AST):
    specifiers: list[AST]
    source: AST


@_dataclass
class ImportNamespaceSpecifier(AST):
    local: AST
