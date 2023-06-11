from vaste import (
    VasteApp,
    component,
)

from vaste.vue.lib.html import *
from vaste.vue.lib.svg import *

import os


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

    class server_methods:

        def test(self):
            return os.listdir()

    def render(self):
        return div([
            nav(
                Class="navbar navbar-primary bg-primary",
                children=[
                    a(
                        Class="navbar-brand",
                        href="#",
                        children=[
                            "Vaste Test"
                            # js.bom.document.baseURI
                        ],
                    ),
                ],
            ),
            div(
                children=[
                    button(
                        children=[
                            "My ", self.lool," count : ", self.count,
                        ],
                        onClick=self.inc,
                        Class="btn btn-primary",
                    ),
                    button(
                        children=["RESET"],
                        onClick=self.reset,
                        Class="btn btn-danger",
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


print(MyComponent)
print(MyComponent.unparse())

app = VasteApp(MyComponent)
