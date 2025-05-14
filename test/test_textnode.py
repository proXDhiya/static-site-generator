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

if __name__ == "__main__":
    unittest.main()
