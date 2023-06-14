from vaste import (
    VasteApp,
    component,
)

from vaste.vue.lib.html import *
from vaste.vue.lib.svg import *

from vaste.npm.lib import node_module
from vaste.js.lib.bom import location, WebSocket

import os

import fastapi


element = node_module.get(
    "element-plus",
    extra_files=[
        "element-plus/dist/index.css"
    ],
)

vue = node_module.get("vue")
vuerouter = node_module.get("vue-router")

new_WebSocket = WebSocket.new

@component
class MyNav:

    def data(self):
        self.title = "TITLE"
    
    class methods:
        
        def dummy(self):
            self.title

    def render(self):
        return vue.h(
            element.ElMenu,
            { "mode": "horizontal" },
            [
                vue.h(
                    vuerouter.RouterLink,
                    { "to": "/" },
                    [vue.h(
                        element.ElMenuItem,
                        {},
                        [self.title]
                    )],
                ),
                vue.h(
                    vuerouter.RouterLink,
                    { "to": "/miew" },
                    [vue.h(
                        element.ElMenuItem,
                        {},
                        ["MIEW"]
                    )],
                ),
            ],
        )

LOOL = "MIEW"
COUNT = 0


@component
class MyComponent:

    def data(self):
        self.count = self.get_count()
        self.lool = "MIEW"

    class methods:

        def connect(self):
            self.ws = new_WebSocket("ws://"+location.host+"/ws")

        def send(self):
            self.ws.send("SEND")

    class server_methods:

        def get_count(self):
            global COUNT
            return COUNT

        def inc(self):
            global COUNT
            COUNT += 10
            self.count = COUNT
            return COUNT

        def dec(self):
            global COUNT
            COUNT -= 2
            self.count = COUNT
            return COUNT

        def reset(self):
            global COUNT
            COUNT = 0
            self.count = COUNT
            return COUNT

        def test(self):
            return os.listdir()

    def render(self):
        return div([
            vue.h(
                MyNav,
                {},
                [],
            ),
            div(
                children=[
                    vue.h(
                        element.ElButton,
                        {"onClick": self.inc},
                        [
                            "My ", self.lool," count : ", self.count,
                        ],
                    ),
                    vue.h(
                        element.ElButton,
                        {"onClick": self.reset},
                        ["RESET"],
                    ),
                    vue.h(
                        element.ElButton,
                        {"onClick": self.connect},
                        ["CONNECT"],
                    ),
                    vue.h(
                        element.ElButton,
                        {"onClick": self.send},
                        ["SEND"],
                    ),
                    svg(
                        children=[
                            rect(
                                x=0,
                                y=0,
                                width=100,
                                height=self.count + 50,
                                onClick=self.dec,
                            )
                        ],
                    ),
                    ul(
                        children=[
                            li(
                                children=[path],
                                Class="list-group-item",
                            )
                            for path in self.test()
                        ],
                        Class="list-group",
                    ),
                ],
            ),
        ])


@component
class MyComponent2:

    def render(self):
        return div([
            vue.h(
                MyNav,
                {},
                [],
            ),
            div(["Other component"]),
        ])


# print(MyComponent)
# print(MyComponent.unparse())

app = VasteApp()

app.add_component_route("/miew", MyComponent)

app.add_component_route("/", MyComponent)


@app.websocket("/ws")
async def websocket_endpoint(websocket: fastapi.WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
