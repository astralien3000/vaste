import ast
import inspect

from vaste import js

from vaste.js.transformer.default import DefaultTransformer
from vaste.js.transformer.methods import MethodsTransformer

from vaste.js.decorator.program import program

from vaste.js.builtin import *
from vaste.vue.html import *
from vaste.vue.svg import *

from vaste.vue.decorator.component import component

from vaste.app import VasteApp


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
            nav(
                Class="navbar navbar-primary bg-primary",
                children=[
                    a(
                        Class="navbar-brand",
                        href="#",
                        children=[
                            document.baseURI
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
                ],
            ),
        ])


app = VasteApp(MyComponent)
