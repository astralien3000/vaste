from . import ast as _ast

from types import NoneType as _NoneType


def unparse(ast_obj: _ast.AST):
    return globals()[f"_unparse_{ast_obj.__class__.__name__}"](ast_obj)


def _unparse_Program(ast_obj: _ast.Program):
        return "".join([
            unparse(stmt) for stmt in ast_obj.body
        ])


def _unparse_VariableDeclaration(ast_obj: _ast.VariableDeclaration):
        return f"""{ast_obj.kind} {
            ",".join([
                unparse(vdecl)
                for vdecl in ast_obj.declarations
            ])
        };"""


def _unparse_ExportNamedDeclaration(ast_obj: _ast.ExportNamedDeclaration):
        return f"""export {
            ",".join([
                unparse(vdecl)
                for vdecl in ast_obj.declarations
            ])
        };"""


def _unparse_ExportDefaultDeclaration(ast_obj: _ast.ExportDefaultDeclaration):
        return f"""export default {
            unparse(ast_obj.declaration)
        };"""


def _unparse_VariableDeclarator(ast_obj: _ast.VariableDeclarator):
        return f"""{unparse(ast_obj.id)}={unparse(ast_obj.init)}"""


def _unparse_Identifier(ast_obj: _ast.Identifier):
        return ast_obj.name


def _unparse_Literal(ast_obj: _ast.Literal):
        match ast_obj.value:
            case _NoneType():
                return "null"
            case str():
                return f'"{ast_obj.value}"'
            case bool():
                return "true" if ast_obj.value else "false"
        return str(ast_obj.value)


def _unparse_FunctionDeclaration(ast_obj: _ast.FunctionDeclaration):
        return f"""function {unparse(ast_obj.id)}({
            ",".join([
                unparse(param)
                for param in ast_obj.params
            ])
        }){unparse(ast_obj.body)};"""


def _unparse_BlockStatement(ast_obj: _ast.BlockStatement):
        return f"""{{{
            "".join([
                unparse(stmt) for stmt in ast_obj.body
            ])
        }}}"""


def _unparse_ExpressionStatement(ast_obj: _ast.ExpressionStatement):
        return f"{unparse(ast_obj.expression)};"


def _unparse_CallExpression(ast_obj: _ast.CallExpression):
        return f"""{unparse(ast_obj.callee)}({",".join([
            unparse(arg)
            for arg in ast_obj.arguments
        ])})"""


def _unparse_NewExpression(ast_obj: _ast.NewExpression):
        return f"""new {unparse(ast_obj.callee)}({",".join([
            unparse(arg)
            for arg in ast_obj.arguments
        ])})"""


def _unparse_MemberExpression(ast_obj: _ast.MemberExpression):
        if ast_obj.computed:
            return f"{unparse(ast_obj.object)}[{unparse(ast_obj.property)}]"
        return f"{unparse(ast_obj.object)}.{unparse(ast_obj.property)}"


def _unparse_ArrowFunctionExpression(ast_obj: _ast.ArrowFunctionExpression):
        return f"""({
            ",".join([
                unparse(param)
                for param in ast_obj.params
            ])
        })=>{unparse(ast_obj.body)}"""


def _unparse_BinaryExpression(ast_obj: _ast.BinaryExpression):
        return f"{unparse(ast_obj.left)}{ast_obj.operator}{unparse(ast_obj.right)}"


def _unparse_AssignmentExpression(ast_obj: _ast.AssignmentExpression):
        return f"{unparse(ast_obj.left)}{ast_obj.operator}{unparse(ast_obj.right)}"


def _unparse_ObjectExpression(ast_obj: _ast.ObjectExpression):
        return f"""{{{
            ",".join([
                unparse(prop)
                for prop in ast_obj.properties
            ])
        }}}"""


def _unparse_Property(ast_obj: _ast.Property):
        if ast_obj.method:
            return f"{unparse(ast_obj.key)}{unparse(ast_obj.value)}"
        else:
            return f"{unparse(ast_obj.key)}:{unparse(ast_obj.value)}"


def _unparse_FunctionExpression(ast_obj: _ast.FunctionExpression):
        return f"""({
            ",".join([
                unparse(param)
                for param in ast_obj.params
            ])
        }){unparse(ast_obj.body)}"""


def _unparse_ReturnStatement(ast_obj: _ast.ReturnStatement):
        return f"return {unparse(ast_obj.argument)};"


def _unparse_ArrayExpression(ast_obj: _ast.ArrayExpression):
        return f"""[{
            ",".join([
                unparse(elem)
                for elem in ast_obj.elements
            ])
        }]"""


def _unparse_ImportDeclaration(ast_obj: _ast.ImportDeclaration):
        if len(ast_obj.specifiers) == 0:
            return f"""import {
                unparse(ast_obj.source)
            };"""
        return f"""import {
            ",".join([
                unparse(spec)
                for spec in ast_obj.specifiers
            ])
        } from {
            unparse(ast_obj.source)
        };"""


def _unparse_ImportNamespaceSpecifier(ast_obj: _ast.ImportNamespaceSpecifier):
        return f"""* as {
            unparse(ast_obj.local)
        }"""


def _unparse_ThisExpression(ast_obj: _ast.ThisExpression):
        return "this"
