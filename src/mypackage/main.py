from mypackage.transformers.transformer import split_nodes_delimiter
from mypackage.nodes.textnode import TextNode, TextType
from mypackage.nodes.htmlnode import ParentNode, LeafNode


def main():
    node = ParentNode(
        tag="div",
        children=[
            LeafNode(tag="p", value="Hello world"),
            LeafNode(tag="a", value="Click Me!", props={'href': 'https://dhiya.me'}),
        ],
        props={'style': '{ margin: 0 auto; text-align: center; }'}
    )
    print(node.to_html())

    node = TextNode('Click [here](https://dhiya.me) please', TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], '[', TextType.LINK)
    print(new_nodes)
