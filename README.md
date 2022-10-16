# Vaste

Vue.js in python !

## Introduction

Vaste is a python library for building web interfaces.
It enables to use the power of the Vue.js framework, from server-side python.

## Basic example

```python
from vaste import (
    VasteApp,
    component,
)

from vaste.vue.lib.html import button


@component
class MyComponent:

    def data(self):
        self.count = 0

    class methods:

        def inc(self):
            self.count += 1

    def render(self):
        return button(
            children=[
                "Count : ", self.count,
            ],
            onClick=self.inc,
        )

app = VasteApp(MyComponent)

```