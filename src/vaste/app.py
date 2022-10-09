import fastapi

from vaste import js


class VasteApp(fastapi.FastAPI):

    def __init__(self, component):
        super().__init__()
        self.component = component
        
        @self.get("/", response_class=fastapi.responses.HTMLResponse)
        def get_root():
            return f"""
                <html>
                    <head>
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
                        <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>
                    </head>
                    <body>
                        <div id="app"></div>
                        <script>{
                            js.ast.unparse(
                                self.ast
                            )
                        }</script>
                    </body>
                </html>
            """

    @property
    def ast(self):
        return js.ast.Program([
            js.ast.ExpressionStatement(
                js.ast.CallExpression(
                    callee=js.ast.MemberExpression(
                        object=js.ast.CallExpression(
                            callee=js.ast.MemberExpression(
                                object=js.ast.Identifier("Vue"),
                                property=js.ast.Identifier("createApp"),
                            ),
                            arguments=[
                                self.component.ast,
                            ],
                        ),
                        property=js.ast.Identifier("mount"),
                    ),
                    arguments=[
                        js.ast.Literal("#app"),
                    ],
                )
            )
        ])
