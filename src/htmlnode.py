class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ""
        if self.props is None or not self.props:
            return string
        for key, value in self.props.items():
            string = string + f' {key}="{value}"'
        return string

    def __eq__(self, other):
        return (self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag is None:
            return str(self.value)
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        elif self.children is None:
            raise ValueError("By definition, all parent nodes must have at least one child")
        else:
            beginning = f'<{self.tag}{self.props_to_html()}>'
            end = f'</{self.tag}>'
            middle = "".join(child.to_html() for child in self.children)
            return f'{beginning}{middle}{end}'