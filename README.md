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

## Disclaimer

This library is still in early development, the interface is not stable and can change drastically.

## Quickstart

### Clone repo

```bash
git clone https://github.com/astralien3000/vaste.git
cd vaste
```

### Install dependencies

```bash
python -m pip install -e .
```

An ASGI-compatible webserver is also needed :

```bash
python -m pip install uvicorn
```

### Run examples

#### Web

To run the basic example shown in this README :

```bash
python -m uvicorn basic:app --reload
```

A more complex showcase :

```bash
python -m uvicorn main:app --reload
```

Then [http://127.0.0.1:8000](http://127.0.0.1:8000) can be visited.

#### Node

Server-side javascript can also be run :

```bash
python example.py
```

I still don't know what would be the use of this but it is possible ! ^^
