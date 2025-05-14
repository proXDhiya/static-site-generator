from mypackage.nodes.textnode import TextNode, TextType
import unittest

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a second text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_nonvalid_type(self):
        with self.assertRaises(TypeError):
            TextNode('text', 'potato')

    def test_valid_type(self):
        try:
            TextNode('text', TextType.BOLD)
        except TypeError:
            self.fail("TextNode raised TypeError unexpectedly!")

    def test_empty_url(self):
        node = TextNode('', TextType.LINK, url='https://www.google.com')
        self.assertEqual(node.url, 'https://www.google.com')

    def test_repr(self):
        node = TextNode("sample", TextType.ITALIC, url="http://example.com")
        expected_repr = "TextNode(sample, TextType.ITALIC, http://example.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_eq_different_url(self):
        node1 = TextNode("text", TextType.LINK, url="http://a.com")
        node2 = TextNode("text", TextType.LINK, url="http://b.com")
        self.assertNotEqual(node1, node2)

    def test_eq_different_type(self):
        node1 = TextNode("text", TextType.BOLD)
        node2 = TextNode("text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
