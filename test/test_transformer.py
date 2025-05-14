import unittest
from mypackage.transformers.transformer import split_nodes_delimiter, text_node_to_html_node
from mypackage.nodes.textnode import TextNode, TextType
from mypackage.nodes.htmlnode import LeafNode


class TestTransformerExtended(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = TextNode("hello", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "hello")
        self.assertIsNone(html_node.tag)

    def test_text_node_to_html_node_link(self):
        node = TextNode("click", TextType.LINK, url="http://url.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props.get("href"), "http://url.com")

    def test_split_nodes_delimiter_link(self):
        text = "Click [here](http://example.com) now"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_delimiter([node], '[', TextType.LINK)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "http://example.com")

    def test_split_nodes_delimiter_other_type(self):
        text = "Some *bold* text"
        node = TextNode(text, TextType.TEXT)
        result = split_nodes_delimiter([node], '*', TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, "bold")


if __name__ == "__main__":
    unittest.main()
