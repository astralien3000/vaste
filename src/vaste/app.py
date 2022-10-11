import fastapi
from fastapi.responses import HTMLResponse

from vaste import js
from vaste.js.builtin import JsObjectRef

from collections import deque


class Unquote:
    def __init__(self):
        self.data = deque()

    def __call__(self, arg):
        self.data.append(arg)
    
    def pop(self):
        return self.data.popleft()


class VasteApp(fastapi.FastAPI):

    def __init__(self, component):
        super().__init__()
        self.component = component

        @self.get("/")
        def get_root():
            return HTMLResponse(f"""
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
            """)

    @property
    def ast(self):
        Vue = JsObjectRef(js.ast.Identifier("Vue"))
        UNQUOTE = Unquote()

        @js.fprogram(UNQUOTE)
        class MainProgram:
            Vue.createApp(
                UNQUOTE(self.component.ast)
            ).mount("#app")

        return MainProgram
