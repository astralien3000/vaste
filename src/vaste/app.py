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

from vaste.js.macro.macro import JsMacro


def append_html(path):
    if path[-1] == "/":
        return path + "index.html"
    else:
        return path + ".html"


class ComponentRoutesJsMacro(JsMacro):

    def __init__(self, component_routes):
        self.component_routes = component_routes
    
    class Transformer(JsMacro.Transformer):
        def transform(self, py_ast):
            return js.ast.ArrayExpression([
                js.ast.ObjectExpression([
                    js.ast.Property(
                        key=js.ast.Identifier("path"),
                        value=js.ast.Literal(component_route["path"]),
                    ),
                    js.ast.Property(
                        key=js.ast.Identifier("alias"),
                        value=js.ast.Literal(append_html(component_route["path"])),
                    ),
                    js.ast.Property(
                        key=js.ast.Identifier("component"),
                        value=js.ast.Identifier(component_route["component"].name),
                    ),
                ])
                for component_route in self.macro.component_routes
            ])

    def save(self):
        for component_route in self.component_routes:
            component_route["component"].save()

    @property
    def import_list(self):
        return [
            stmt
            for component_route in self.component_routes
            for stmt in component_route["component"].import_list
        ]


class VasteApp(fastapi.FastAPI):

    def __init__(self, component = vuerouter.RouterView):
        super().__init__()
        self.component = component
        self.component_routes = []

        @self.on_event("startup")
        def startup():
            with open("index.html", "w") as f:
                f.write(str(self.index))

            self.ast.save()

            os.system("node node_modules/vite-ssg/bin/vite-ssg.js build")

            self.mount("/", StaticFiles(directory="dist", html=True))

    def add_component_route(self, path, component):
        self.component_routes.append({
            "path": path,
            "component": component,
        })

        self.mount(f"/api", component.api)

        @self.get(path)
        def get_path():
            with open(f"dist/{append_html(path)}", "r") as file:
                return fastapi.responses.HTMLResponse(file.read())

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
        routes = ComponentRoutesJsMacro(self.component_routes)

        @js.program
        class MainProgram:
            createApp = vitessg.ViteSSG(
                component,
                {
                    "routes": routes,
                },
            )

        # print(MainProgram)
        # print(MainProgram.unparse())

        return MainProgram
