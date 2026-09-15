class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self):
        raise NotImplementedError
        
    def props_to_html(self):
        if self.props is not None:
            props = ''
            for key, item in self.props:
                props += f' {key}={item} '
            return props
        return ''

    def __repr__(self):
        return f'HTMLNode(f{self.tag}, f{self.value}, f{self.children}, f{self.props})'