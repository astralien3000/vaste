import fastapi
from fastapi.staticfiles import StaticFiles

from vaste import js

from vaste import html

import os

from vaste.js.macro.program import ProgramJsMacro

class ExtPrgJsMacro(ProgramJsMacro):
    @property
    def filename(self):
        return self.name

vue = ExtPrgJsMacro("vue", None, [])


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

        self.mount("", StaticFiles(directory="dist", html=True))

    @property
    def index(self):
        return  html.html([
            html.head([
                html.link(
                    rel="stylesheet",
                    href="main.scss",
                ),
            ]),
            html.body([
                html.div(id="app"),
                html.script(
                    src="main.js",
                    type="module",
                )
            ])
        ])

    @property
    def ast(self):

        @js.program
        class MainProgram:
            vue.createApp(
                js.lang.inject_ast(self.component.ast)
            ).mount("#app")

        print(MainProgram)
        print(MainProgram.unparse())

        return MainProgram
