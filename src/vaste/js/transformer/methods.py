from .default import *


class MethodsTransformer(DefaultTransformer):

    def transform(self, py_ast):
        match py_ast:
            case ast.Module([module_cls]):
                return self.transform(module_cls)
            case ast.ClassDef("module", [], [], [methods_cls], []):
                return self.transform(methods_cls)
            case ast.ClassDef("methods", [], [], body, []):
                return js.ast.Property(
                    key=js.ast.Identifier("methods"),
                    value=js.ast.ObjectExpression([
                        self.transform(stmt)
                        for stmt in body
                    ]),
                )
            case ast.FunctionDef(name, ast.arguments([], [ast.arg("self"), *args]), body, []):
                return js.ast.Property(
                    key=js.ast.Identifier(name),
                    value=js.ast.FunctionExpression(
                        params=[
                            self.transform(arg)
                            for arg in args
                        ],
                        body=js.ast.BlockStatement([
                            self.transform(stmt)
                            for stmt in body
                        ])
                    ),
                    method=True,
                )
            case ast.AugAssign(target, op, value):
                return js.ast.ExpressionStatement(
                    js.ast.AssignmentExpression(
                        left=self.transform(target),
                        operator=self.transform(op)+"=",
                        right=self.transform(value),
                    ),
                )
            case ast.Assign([target], value):
                return js.ast.ExpressionStatement(
                    js.ast.AssignmentExpression(
                        left=self.transform(target),
                        operator="=",
                        right=self.transform(value),
                    ),
                )
            case ast.Add():
                return "+"
            case ast.Name("self"):
                return js.ast.Identifier(
                    name="this",
                )
        return DefaultTransformer.transform(self, py_ast)
