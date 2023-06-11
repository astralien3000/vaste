from vaste import (
    VasteApp,
    component,
)

from vaste.vue.lib.html import *
from vaste.vue.lib.svg import *

import os


LOOL = "MIEW"
COUNT = 0


@component
class MyComponent:

    def data(self):
        self.count = self.get_count()
        self.lool = "MIEW"

    class methods:

        def inc(self):
            self.count = self.send_inc()

        def dec(self):
            self.count = self.send_dec()

        def reset(self):
            self.count = self.send_reset()

    class server_methods:

        def get_count(self):
            global COUNT
            return COUNT

        def send_inc(self):
            global COUNT
            COUNT += 10
            return COUNT

        def send_dec(self):
            global COUNT
            COUNT -= 2
            return COUNT

        def send_reset(self):
            global COUNT
            COUNT = 0
            return COUNT

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
