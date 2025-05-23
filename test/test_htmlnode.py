from mypackage.nodes.htmlnode import HTMLNode, LeafNode, ParentNode
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode(tag="p", value="Hello world", children=None, props={"color": "red"})
        node2 = HTMLNode(tag="p", value="Hello world", children=None, props={"color": "red"})
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode(
            tag="p",
            value="Hello world",
            children=None,
            props={"color": "red"}
        )
        node2 = HTMLNode(
            tag="ul",
            value=None,
            children=[
                HTMLNode(tag="li", value="task 1"),
                HTMLNode(tag="li", value="task 2"),
            ],
            props={"color": "red"}
        )
        self.assertNotEqual(node1, node2)

    def test_no_value_or_children(self):
        with self.assertRaises(ValueError):
            HTMLNode(tag="p", value=None, children=None)

    def test_props_is_not_dict(self):
        with self.assertRaises(TypeError):
            HTMLNode(tag="p", value="Hello world", props=['color', 'red'])

    def test_props_is_dict(self):
        node = HTMLNode(tag="p", value="Hello world", props={"color": "red"})
        self.assertEqual(node.props, {"color": "red"})

    def test_children_is_not_list(self):
        with self.assertRaises(TypeError):
            HTMLNode(tag="p", value="Hello world", children={'color': 'red'})

    def test_children_is_not_list_of_HTMLNodes(self):
        with self.assertRaises(TypeError):
            HTMLNode(tag="p", value="Hello world", children=[{'color': 'red'}])

    def test_children_is_list_of_HTMLNodes(self):
        node = HTMLNode(
            tag="ul",
            value=None,
            children=[
                HTMLNode(tag="li", value="task 1"),
                HTMLNode(tag="li", value="task 2"),
            ],
            props={"color": "red"}
        )
        self.assertEqual(node.children, [
            HTMLNode(tag="li", value="task 1"),
            HTMLNode(tag="li", value="task 2"),
        ])

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_leaf_node_value_none_for_non_img(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_parent_node_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_props_to_html_empty(self):
        node = LeafNode("span", "text", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple(self):
        node = LeafNode("a", "link", props={"href": "url", "target": "_blank"})
        props_html = node.props_to_html()
        # Order of props is not guaranteed, so test both possibilities
        self.assertTrue(
            props_html == 'href="url" target="_blank"' or props_html == 'target="_blank" href="url"'
        )


if __name__ == "__main__":
    unittest.main()
