from . import ast as _ast

from types import NoneType as _NoneType


def unparse(node: _ast.AST):
    return globals()[f"_unparse_{node.__class__.__name__}"](node)


def _unparse_Program(node: _ast.Program):
    return "".join([
        unparse(stmt) for stmt in node.body
    ])


def _unparse_VariableDeclaration(node: _ast.VariableDeclaration):
    return f"""{node.kind} {
        ",".join([
            unparse(vdecl)
            for vdecl in node.declarations
        ])
    };"""


def _unparse_ExportNamedDeclaration(node: _ast.ExportNamedDeclaration):
    return f"""export {
        ",".join([
            unparse(vdecl)
            for vdecl in node.declarations
        ])
    };"""


def _unparse_ExportDefaultDeclaration(node: _ast.ExportDefaultDeclaration):
    return f"""export default {
        unparse(node.declaration)
    };"""


def _unparse_VariableDeclarator(node: _ast.VariableDeclarator):
    return f"""{unparse(node.id)}={unparse(node.init)}"""


def _unparse_Identifier(node: _ast.Identifier):
    return node.name


def _unparse_Literal(node: _ast.Literal):
    match node.value:
        case _NoneType():
            return "null"
        case str():
            return f'"{node.value}"'
        case bool():
            return "true" if node.value else "false"
    return str(node.value)


def _unparse_FunctionDeclaration(node: _ast.FunctionDeclaration):
    return f"""function {unparse(node.id)}({
        ",".join([
            unparse(param)
            for param in node.params
        ])
    }){unparse(node.body)};"""


def _unparse_BlockStatement(node: _ast.BlockStatement):
    return f"""{{{
        "".join([
            unparse(stmt) for stmt in node.body
        ])
    }}}"""


def _unparse_ExpressionStatement(node: _ast.ExpressionStatement):
    return f"{unparse(node.expression)};"


def _unparse_CallExpression(node: _ast.CallExpression):
    return f"""{unparse(node.callee)}({",".join([
        unparse(arg)
        for arg in node.arguments
    ])})"""


def _unparse_NewExpression(node: _ast.NewExpression):
    return f"""new {unparse(node.callee)}({",".join([
        unparse(arg)
        for arg in node.arguments
    ])})"""


def _unparse_MemberExpression(node: _ast.MemberExpression):
    if node.computed:
        return f"{unparse(node.object)}[{unparse(node.property)}]"
    return f"{unparse(node.object)}.{unparse(node.property)}"


def _unparse_ArrowFunctionExpression(node: _ast.ArrowFunctionExpression):
    return f"""({
        ",".join([
            unparse(param)
            for param in node.params
        ])
    })=>{unparse(node.body)}"""


def _unparse_BinaryExpression(node: _ast.BinaryExpression):
    return f"{unparse(node.left)}{node.operator}{unparse(node.right)}"


def _unparse_AssignmentExpression(node: _ast.AssignmentExpression):
    return f"{unparse(node.left)}{node.operator}{unparse(node.right)}"


def _unparse_ObjectExpression(node: _ast.ObjectExpression):
    return f"""{{{
        ",".join([
            unparse(prop)
            for prop in node.properties
        ])
    }}}"""


def _unparse_Property(node: _ast.Property):
    if node.method:
        return f"{unparse(node.key)}{unparse(node.value)}"
    else:
        return f"{unparse(node.key)}:{unparse(node.value)}"


def _unparse_FunctionExpression(node: _ast.FunctionExpression):
    return f"""({
        ",".join([
            unparse(param)
            for param in node.params
        ])
    }){unparse(node.body)}"""


def _unparse_ReturnStatement(node: _ast.ReturnStatement):
    return f"return {unparse(node.argument)};"


def _unparse_ArrayExpression(node: _ast.ArrayExpression):
    return f"""[{
        ",".join([
            unparse(elem)
            for elem in node.elements
        ])
    }]"""


def _unparse_ImportDeclaration(node: _ast.ImportDeclaration):
    if len(node.specifiers) == 0:
        return f"""import {
            unparse(node.source)
        };"""
    return f"""import {
        ",".join([
            unparse(spec)
            for spec in node.specifiers
        ])
    } from {
        unparse(node.source)
    };"""


def _unparse_ImportNamespaceSpecifier(node: _ast.ImportNamespaceSpecifier):
    return f"""* as {
        unparse(node.local)
    }"""


def _unparse_ThisExpression(node: _ast.ThisExpression):
    return "this"


def _unparse_IfStatement(node: _ast.IfStatement):
    if node.alternate:
        return f"""if({unparse(node.test)}){unparse(node.consequent)}else{
            unparse(node.alternate)
        }"""
    return f"if({unparse(node.test)}){unparse(node.consequent)}"


def _unparse_UnaryExpression(node: _ast.UnaryExpression):
    if node.prefix:
        return f"{node.operator}{unparse(node.argument)}"
    else:
        return f"{unparse(node.argument)}{node.operator}"
