import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a test paragraph", None, None)
        node2 = HTMLNode("p", "This is a test paragraph", None, None)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("p", "This is a test paragraph", None, None)
        node2 = HTMLNode("a", "This is a test link", None, {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    def test_props_to_html_one(self):
        props = HTMLNode("p", "This is a test paragraph", None, None).props_to_html()
        props2 = HTMLNode("a", "This is a test link", None, {"href": "https://www.google.com"}).props_to_html()
        self.assertNotEqual(props, props2)

    def test_props_to_html_two(self):
        props = HTMLNode("p", "This is a test paragraph", None, {"href": "https://www.google.com", "target": "_blank"}).props_to_html()
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(props, expected_output)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        expected_output = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a test link", {"href": "https://www.google.com"})
        expected_output = '<a href="https://www.google.com">This is a test link</a>'
        self.assertEqual(node.to_html(), expected_output)

    def test_leaf_to_html_tag_none(self):
        node = LeafNode(None, "This is a none-tag test", None)
        expected_output = 'This is a none-tag test'
        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html() 

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

if __name__ == "__main__":
    unittest.main()