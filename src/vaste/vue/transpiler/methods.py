from ...js.transpiler.macro import *


class MethodsTranspiler(MacroExpansionTranspiler):
    def transpile(self, py_ast):
        match py_ast:
            case py.ast.Module([module_cls]):
                return self.transpile(module_cls)
            case py.ast.ClassDef("module", [], [], [methods_cls], []):
                return self.transpile(methods_cls)
            case py.ast.ClassDef("methods", [], [], body, []):
                return js.ast.Property(
                    key=js.ast.Identifier("methods"),
                    value=js.ast.ObjectExpression(
                        [self.transpile(stmt) for stmt in body]
                    ),
                )
            case py.ast.FunctionDef(
                name, py.ast.arguments([], [py.ast.arg("self"), *args]), body, []
            ):
                return js.ast.Property(
                    key=js.ast.Identifier(name),
                    value=js.ast.FunctionExpression(
                        params=[self.transpile(arg) for arg in args],
                        body=js.ast.BlockStatement(
                            [self.transpile(stmt) for stmt in body]
                        ),
                    ),
                    method=True,
                )
            case py.ast.AugAssign(target, op, value):
                return js.ast.ExpressionStatement(
                    js.ast.AssignmentExpression(
                        left=self.transpile(target),
                        operator=self.transpile(op) + "=",
                        right=self.transpile(value),
                    ),
                )
            case py.ast.Assign([py.ast.Name(name)], value):
                return js.ast.VariableDeclaration(
                    [
                        js.ast.VariableDeclarator(
                            id=js.ast.Identifier(name),
                            init=self.transpile(value),
                        ),
                    ]
                )
            case py.ast.Assign([target], value):
                return js.ast.ExpressionStatement(
                    js.ast.AssignmentExpression(
                        left=self.transpile(target),
                        operator="=",
                        right=self.transpile(value),
                    ),
                )
            case py.ast.Add():
                return "+"
            case py.ast.Sub():
                return "-"
            case py.ast.Name("self"):
                return js.ast.Identifier(
                    name="this",
                )
        return super().transpile(py_ast)
