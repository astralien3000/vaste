import fastapi
from fastapi.staticfiles import StaticFiles

from vaste import js

from vaste import html

from vaste.npm.lib import node_module

import os


vue = node_module.get("vue")
vuerouter = node_module.get("vue-router")
vite = node_module.get("vite")
vitessg = node_module.get("vite-ssg")
vitessgsinglepage = node_module.get_file("vite-ssg/single-page")


class VasteApp(fastapi.FastAPI):

    def __init__(self, component):
        super().__init__()
        self.component = component

        with open("index.html", "w") as f:
            f.write(str(self.index))

        self.ast.save()

        os.system("node node_modules/vite-ssg/bin/vite-ssg.js build")

        self.mount("", StaticFiles(directory="dist", html=True))

    @property
    def index(self):
        return  html.html([
            html.head([
                html.script(
                    src=self.ast.filename,
                    type="module",
                ),
            ]),
            html.body([
                html.div(id="app"),
            ])
        ])

    @property
    def ast(self):
        component = self.component

        @js.program
        class MainProgram:
            createApp = vitessgsinglepage.ViteSSG(
                component
            )

        # print(MainProgram)
        # print(MainProgram.unparse())

        return MainProgram
