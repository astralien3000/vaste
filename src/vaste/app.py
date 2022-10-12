import fastapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from vaste import js
from vaste.js.builtin import JsObjectRef

from collections import deque

from vaste import html

import os


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

        with open("index.html", "w") as f:
            f.write(str(self.index))

        with open("main.js", "w") as f:
            f.write(js.ast.unparse(self.ast))

        with open("main.scss", "w") as f:
            f.write("""@import "bootstrap/scss/bootstrap";""")

        os.system("node node_modules/vite/bin/vite.js build")

        # @self.get("/")
        # def get_root():
        #     return HTMLResponse(self.index)

        self.mount("", StaticFiles(directory="dist", html=True))

    @property
    def index(self):
        return  html.html([
            html.head([
                # html.script(
                #     src="https://unpkg.com/vue@3/dist/vue.global.js",
                # ),
                html.link(
                    rel="stylesheet",
                    href="main.scss",
                ),
            ]),
            html.body([
                html.div(id="app"),
                # html.script([
                #     js.ast.unparse(
                #         self.ast
                #     )
                # ])
                html.script(
                    src="main.js",
                    type="module",
                )
            ])
        ])

    @property
    def ast(self):
        jsimport = JsObjectRef(js.ast.Identifier("import"))
        UNQUOTE = Unquote()

        @js.fprogram(UNQUOTE)
        class MainProgram:
            Vue = jsimport("vue")

            Vue.createApp(
                UNQUOTE(self.component.ast)
            ).mount("#app")

        return MainProgram
