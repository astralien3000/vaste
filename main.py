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

app = VasteApp(MyComponent)
