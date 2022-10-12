
class HTMLElement:

    def __init__(self, type, props, children, no_end_tag):
        self.type = type
        self.props = props
        self.children = children
        self.no_end_tag = no_end_tag
    
    def __str__(self):
        if self.no_end_tag:
            return f"""<{
                " ".join([self.type] + [
                    f'{k}="{v}"'
                    for k, v in self.props.items()
                ])
            }/>"""
        else:
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
    def __init__(self, name, no_end_tag=False):
        self.name = name
        self.no_end_tag = no_end_tag

    def __call__(self, children = [], **kwargs):
        return HTMLElement(
            type=self.name,
            children=children,
            props=kwargs,
            no_end_tag=self.no_end_tag,
        )


html = HTMLElementFactory("html")
head = HTMLElementFactory("head")
script = HTMLElementFactory("script")
link = HTMLElementFactory("link", True)
body = HTMLElementFactory("body")
div = HTMLElementFactory("div")
