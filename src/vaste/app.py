import fastapi
from fastapi.responses import HTMLResponse

from vaste import js
from vaste.js.builtin import JsObjectRef

from collections import deque

from vaste import html


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
            return HTMLResponse(
                html.html([
                    html.head([
                        html.script(
                            src="https://unpkg.com/vue@3/dist/vue.global.js",
                        ),
                    ]),
                    html.body([
                        html.div(id="app"),
                        html.script([
                            js.ast.unparse(
                                self.ast
                            )
                        ])
                    ])
                ])
            )

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
