from mypackage.transformers.transformer import split_nodes_delimiter, split_nodes_image
from mypackage.nodes.textnode import TextNode, TextType
from mypackage.nodes.htmlnode import ParentNode, LeafNode


def main():
    # test 1: Parent node
    node = ParentNode(
        tag="div",
        children=[
            LeafNode(tag="p", value="Hello world"),
            LeafNode(tag="a", value="Click Me!", props={'href': 'https://dhiya.me'}),
        ],
        props={'style': '{ margin: 0 auto; text-align: center; }'}
    )
    print(node.to_html())

    # test 2: Text node with split_nodes_delimiter
    node = TextNode('Click [here](https://dhiya.me) please', TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], '[', TextType.LINK)
    print(new_nodes)

    # test 3: split_nodes_image
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    print(new_nodes)
