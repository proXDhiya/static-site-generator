class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if value is None and children is None:
            raise ValueError('One of value or children must be specified')

        if props is not None and not isinstance(props, dict):
            raise TypeError('props must be a dict')

        if children is not None:
            if not isinstance(children, list):
                raise TypeError('children must be a list')
            if not all(isinstance(child, HTMLNode) for child in children):
                raise TypeError('all children must be instances of HTMLNode')

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        props_result = ""
        for key, value in self.props.items():
            props_result += f'{key}="{value}" '

        return props_result.strip()

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        if self.tag != other.tag:
            return False
        if self.value != other.value:
            return False
        if self.children != other.children:
            return False
        if self.props != other.props:
            return False
        return True

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None and tag != 'img':
            raise ValueError('value cannot be None')

        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value

        props_str = self.props_to_html()
        props_part = f" {props_str}" if props_str else ""

        # Self-closing tag for img
        if self.tag == 'img':
            return f"<{self.tag}{props_part} />"

        return f"<{self.tag}{props_part}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError('tag cannot be None')

        if children is None:
            raise ValueError('children cannot be None')

        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('tag cannot be None')

        children_html = "".join(child.to_html() for child in self.children)

        props_str = self.props_to_html()
        props_part = f" {props_str}" if props_str else ""

        return f"<{self.tag}{props_part}>{children_html}</{self.tag}>"
