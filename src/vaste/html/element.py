
class HTMLElement:

    def __init__(self, type, props, children):
        self.type = type
        self.props = props
        self.children = children
    
    def __str__(self):
        return f"""<{
            " ".join([self.type] + [
                f'{k}="{v}"'
                for k, v in self.props.items()
            ])
        }>{
            "".join([
                str(child) for child in self.children
            ])
        }</{
            self.type
        }>"""
    
    def encode(self, *args, **kwargs):
        return str(self).encode(*args, **kwargs)


class HTMLElementFactory:
    def __init__(self, name):
        self.name = name

    def __call__(self, children = [], **kwargs):
        return HTMLElement(
            type=self.name,
            children=children,
            props=kwargs,
        )


html = HTMLElementFactory("html")
head = HTMLElementFactory("head")
script = HTMLElementFactory("script")
link = HTMLElementFactory("link")
body = HTMLElementFactory("body")
div = HTMLElementFactory("div")
