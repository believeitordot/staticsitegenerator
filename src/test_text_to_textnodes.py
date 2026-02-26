import unittest

from markdown_inline import text_to_textnodes
from textnode import TextNode, TextType

def nodes_as_tuples(nodes):
    """
    Normalize nodes for easy assertions.
    Assumes TextNode has attributes: text, text_type, url (url may be None).
    If your attribute name differs, change it here once.
    """
    return [(n.text, n.text_type, getattr(n, "url", None)) for n in nodes]


class TestTextToTextNodes(unittest.TestCase):
    def test_full_mixed_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        out = text_to_textnodes(text)

        self.assertEqual(
            nodes_as_tuples(out),
            [
                ("This is ", TextType.TEXT, None),
                ("text", TextType.BOLD, None),
                (" with an ", TextType.TEXT, None),
                ("italic", TextType.ITALIC, None),
                (" word and a ", TextType.TEXT, None),
                ("code block", TextType.CODE, None),
                (" and an ", TextType.TEXT, None),
                ("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                (" and a ", TextType.TEXT, None),
                ("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_plain_text_only(self):
        text = "just normal text"
        out = text_to_textnodes(text)

        self.assertEqual(nodes_as_tuples(out), [("just normal text", TextType.TEXT, None)])

    def test_only_delimiters(self):
        text = "**b** _i_ `c`"
        out = text_to_textnodes(text)

        self.assertEqual(
            nodes_as_tuples(out),
            [
                ("b", TextType.BOLD, None),
                (" ", TextType.TEXT, None),
                ("i", TextType.ITALIC, None),
                (" ", TextType.TEXT, None),
                ("c", TextType.CODE, None),
            ],
        )

    def test_only_image(self):
        text = "![alt](https://example.com/a.png)"
        out = text_to_textnodes(text)

        self.assertEqual(
            nodes_as_tuples(out),
            [("alt", TextType.IMAGE, "https://example.com/a.png")],
        )

    def test_only_link(self):
        text = "[name](https://example.com)"
        out = text_to_textnodes(text)

        self.assertEqual(
            nodes_as_tuples(out),
            [("name", TextType.LINK, "https://example.com")],
        )

    def test_multiple_images_and_links(self):
        text = (
            "a ![x](u1) b [y](u2) c ![z](u3) d [w](u4) e"
        )
        out = text_to_textnodes(text)

        self.assertEqual(
            nodes_as_tuples(out),
            [
                ("a ", TextType.TEXT, None),
                ("x", TextType.IMAGE, "u1"),
                (" b ", TextType.TEXT, None),
                ("y", TextType.LINK, "u2"),
                (" c ", TextType.TEXT, None),
                ("z", TextType.IMAGE, "u3"),
                (" d ", TextType.TEXT, None),
                ("w", TextType.LINK, "u4"),
                (" e", TextType.TEXT, None),
            ],
        )


if __name__ == "__main__":
    unittest.main()