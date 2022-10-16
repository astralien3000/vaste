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
