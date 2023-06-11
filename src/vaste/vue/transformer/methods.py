from ...js.transformer.default import *


class MethodsTransformer(DefaultTransformer):

    def transform(self, py_ast):
        match py_ast:
            case py.ast.Module([module_cls]):
                return self.transform(module_cls)
            case py.ast.ClassDef("module", [], [], [methods_cls], []):
                return self.transform(methods_cls)
            case py.ast.ClassDef("methods", [], [], body, []):
                return js.ast.Property(
                    key=js.ast.Identifier("methods"),
                    value=js.ast.ObjectExpression([
                        self.transform(stmt)
                        for stmt in body
                    ]),
                )
            case py.ast.FunctionDef(name, py.ast.arguments([], [py.ast.arg("self"), *args]), body, []):
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
            case py.ast.AugAssign(target, op, value):
                return js.ast.ExpressionStatement(
                    js.ast.AssignmentExpression(
                        left=self.transform(target),
                        operator=self.transform(op)+"=",
                        right=self.transform(value),
                    ),
                )
            case py.ast.Assign([target], value):
                return js.ast.ExpressionStatement(
                    js.ast.AssignmentExpression(
                        left=self.transform(target),
                        operator="=",
                        right=self.transform(value),
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
        return DefaultTransformer.transform(self, py_ast)
