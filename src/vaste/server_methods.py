from .js.transpiler.default import *


class ServerMethodsTranspiler(DefaultTranspiler):
    def __init__(self, component_name):
        self.component_name = component_name

    def transpile(self, py_ast):
        match py_ast:
            case py.ast.Module([module_cls]):
                return self.transpile(module_cls)
            case py.ast.ClassDef("module", [], [], [methods_cls], []):
                return self.transpile(methods_cls)
            case py.ast.ClassDef("server_methods", [], [], body, []):
                return js.ast.Property(
                    key=js.ast.Identifier("methods"),
                    value=js.ast.ObjectExpression(
                        [self.transpile(stmt) for stmt in body]
                    ),
                )
            case py.ast.FunctionDef(
                name, py.ast.arguments([], [py.ast.arg("self"), *args]), body, []
            ):
                program = js.ast.parse(
                    f"""
                        () => {{
                            var xmlHttp = new XMLHttpRequest();
                            xmlHttp.open(
                                "GET",
                                "api/{self.component_name}/{name}?data=" + JSON.stringify(this.$data),
                                false,
                            );
                            xmlHttp.send(null);
                            const res_obj = JSON.parse(xmlHttp.response);
                            Object.keys(res_obj.data).forEach((k)=>{{
                                this.$data[k] = res_obj.data[k];
                            }});
                            return res_obj.return;
                        }}
                    """
                )
                body = program.body[0].expression.body
                return js.ast.Property(
                    key=js.ast.Identifier(name),
                    value=js.ast.FunctionExpression(
                        params=[self.transpile(arg) for arg in args],
                        body=body,
                    ),
                    method=True,
                )
        return DefaultTranspiler.transpile(self, py_ast)
