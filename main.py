import ast
import inspect


class JsModule:

    def __init__(self, py_ast):
        self.py_ast = py_ast

    def code(self):
        return ast.unparse(self.py_ast)

def javascript(cls):
    cls_ast = ast.parse(
        inspect.getsource(cls),
        mode="exec",
    )
    return JsModule(ast.Module(cls_ast.body[0].body, []))


class JsObj:

    def __getattribute__(self, k):
        return self

    def __call__(self, *args, **kwds):
        return self


window = JsObj()
alert = JsObj()
console = JsObj()
Vue = JsObj()

@javascript
class MyJsModule:
    console.log("test")
    alert("LOOL")

class HtmlTag:
    def __init__(self, name):
        self.name = name
    
    def __call__(*args, **kwargs):
        pass

button = HtmlTag("button")
svg = HtmlTag("svg")
rect = HtmlTag("rect")


class MyComponent:

    def data(self):
        self.count = 1

    def inc(self):
        self.count += 1

    def render(self):
        # return button(
        #     children=[
        #         "count : ",
        #         self.count,
        #     ],
        #     on_click=self.inc,
        # )
        return svg(
            children=rect(
                x=0,
                y=0,
                width=100,
                height=100,
            ),
        )


class DataProxy:

    def __init__(self):
        object.__setattr__(self, "data", {})

    def __setattr__(self, k, v):
        self.data[k] = v
    
    @property
    def vue_data_func(self):
        return f"""
            data() {{
                return {{
                    {",".join([
                        f"{k}: {v}"
                        for k, v in self.data.items()
                    ])}
                }};
            }}
        """


def test(cls):
    dp = DataProxy()
    cls.data(dp)
    print(dp.vue_data_func)

test(MyComponent)

import fastapi

app = fastapi.FastAPI()

@app.get("/", response_class=fastapi.responses.HTMLResponse)
def get_root():
    return f"""
        <html>
            <head>
                <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
            </head>
            <body>
                <div id="app"></div>
                <script>
                    Vue.createApp({{
                        data() {{
                            return {{ count: "0" }}
                        }},
                        methods: {{
                            inc() {{
                                this.count++;
                            }}
                        }},
                        render() {{
                            //return Vue.h("button", {{ onClick: this.inc }}, ["count : ", this.count]);
                            return Vue.h("svg", Vue.h("rect", {{ x: 0, y: 0, width: 100, height: 100 }}));
                        }},
                    }}).mount('#app')
                </script>
            </body>
        </html>
    """
