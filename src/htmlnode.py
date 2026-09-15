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
            for key, item in self.props.items():
                props += f' {key}={item} '
            return props
        return ''

    def __repr__(self):
        return f'HTMLNode(f{self.tag}, f{self.value}, f{self.children}, f{self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError('All leaf nodes must have a value')
        if not self.tag:
            return f'{self.value}'
        if not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            string = ' '
            for key, value in self.props.items():
                string += f'{key}={value} '
            return f'<{self.tag} {string}>{self.value}</{self.tag}>'
            