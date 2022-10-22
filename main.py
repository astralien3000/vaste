from vaste import (
    VasteApp,
    component,
    js,
)

from vaste.vue.lib.html import *
from vaste.vue.lib.svg import *

from vaste.npm.lib import node_module


element = node_module.get(
    "element-plus",
    extra_files=[
        "element-plus/dist/index.css"
    ],
)

vue = node_module.get("vue")
vuerouter = node_module.get("vue-router")


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


@component
class MyComponent:

    def data(self):
        self.count = 0
        self.lool = "MIEW"

    class methods:

        def inc(self):
            self.count += 10

        def dec(self):
            self.count -= 2

        def reset(self):
            self.count = 0

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
                ],
            ),
        ])


# print(MyComponent)
# print(MyComponent.unparse())

app = VasteApp()

app.add_component_route("/miew", MyComponent)

app.add_component_route("/", MyNav)
