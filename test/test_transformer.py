from mypackage.nodes.textnode import TextNode, TextType
from mypackage.transformers.transformer import *
from mypackage.nodes.htmlnode import LeafNode
import unittest


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

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph
    
        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line
    
        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_html_node_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_heading(self):
        md = """
# Heading 1
## Heading 2
### Heading 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_markdown_to_html_node_lists(self):
        md = """
- Item 1
- Item 2
  - Nested item

1. Numbered item
2. Another numbered item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2<ul><li>Nested item</li></ul></li></ul><ol><li>Numbered item</li><li>Another numbered item</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
