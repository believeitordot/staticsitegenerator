import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.LINK, url=None)
        node2 = TextNode("This is a text node", TextType.LINK, url="https://google.com")
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_img(self):
        node = TextNode("", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"alt": "", "src": "https://www.google.com"})
    
    def test_invalid_type(self):
        node = TextNode("Bad node", "not_a_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_link_no_url(self):
        node = TextNode("No link here", TextType.LINK, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"href": None})

    def test_text_empty(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")

    def test_special_chars(self):
        node = TextNode("<b>bold?</b>", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "<b>bold?</b>")

if __name__ == "__main__":
    unittest.main()