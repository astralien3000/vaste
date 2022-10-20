import fastapi
from fastapi.staticfiles import StaticFiles

from vaste import js

from vaste import html

from vaste.npm.lib import node_module

import os


vue = node_module.get("vue")
vite = node_module.get("vite")

element = node_module.get("element-plus")
element_style = node_module.get_file("element-plus/dist/index.css")


class VasteApp(fastapi.FastAPI):

    def __init__(self, component):
        super().__init__()
        self.component = component

        with open("index.html", "w") as f:
            f.write(str(self.index))

        with open("main.js", "w") as f:
            f.write(js.ast.unparse(self.ast))

        os.system("node node_modules/vite/bin/vite.js build")

        self.mount("", StaticFiles(directory="dist", html=True))

    @property
    def index(self):
        return  html.html([
            html.head([
                html.script(
                    src="main.js",
                    type="module",
                ),
            ]),
            html.body([
                html.div(id="app"),
            ])
        ])

    @property
    def ast(self):

        @js.program
        class MainProgram:
            element
            element_style

            vue.createApp(
                js.lang.inject_ast(self.component.ast)
            ).mount("#app")

        print(MainProgram)
        print(MainProgram.unparse())

        return MainProgram
