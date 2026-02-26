import unittest

from markdown_inline import split_nodes_link, split_nodes_image
from textnode import TextNode, TextType

class TestSplitNodesImage(unittest.TestCase):
    def test_non_text_nodes_pass_through(self):
        old_nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode("plain", TextType.TEXT),
        ]
        out = split_nodes_image(old_nodes)

        # First node unchanged
        self.assertEqual(out[0].text, "bold")
        self.assertEqual(out[0].text_type, TextType.BOLD)

        # Second node: no images -> unchanged
        self.assertEqual(out[1].text, "plain")
        self.assertEqual(out[1].text_type, TextType.TEXT)

    def test_text_node_with_no_images_is_kept(self):
        old_nodes = [TextNode("hello world", TextType.TEXT)]
        out = split_nodes_image(old_nodes)

        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].text, "hello world")
        self.assertEqual(out[0].text_type, TextType.TEXT)

    def test_single_image_middle(self):
        old_nodes = [TextNode("hi ![a](u) bye", TextType.TEXT)]
        out = split_nodes_image(old_nodes)

        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in out],
            [
                ("hi ", TextType.TEXT, None),
                ("a", TextType.IMAGE, "u"),
                (" bye", TextType.TEXT, None),
            ],
        )

    def test_single_image_at_start(self):
        old_nodes = [TextNode("![a](u) end", TextType.TEXT)]
        out = split_nodes_image(old_nodes)

        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in out],
            [
                ("a", TextType.IMAGE, "u"),
                (" end", TextType.TEXT, None),
            ],
        )

    def test_single_image_at_end(self):
        old_nodes = [TextNode("start ![a](u)", TextType.TEXT)]
        out = split_nodes_image(old_nodes)

        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in out],
            [
                ("start ", TextType.TEXT, None),
                ("a", TextType.IMAGE, "u"),
            ],
        )

    def test_multiple_images(self):
        old_nodes = [
            TextNode("x ![a](u1) y ![b](u2) z", TextType.TEXT)
        ]
        out = split_nodes_image(old_nodes)

        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in out],
            [
                ("x ", TextType.TEXT, None),
                ("a", TextType.IMAGE, "u1"),
                (" y ", TextType.TEXT, None),
                ("b", TextType.IMAGE, "u2"),
                (" z", TextType.TEXT, None),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_non_text_nodes_pass_through(self):
        old_nodes = [
            TextNode("italic", TextType.ITALIC),
            TextNode("plain", TextType.TEXT),
        ]
        out = split_nodes_link(old_nodes)

        self.assertEqual(out[0].text, "italic")
        self.assertEqual(out[0].text_type, TextType.ITALIC)

        self.assertEqual(out[1].text, "plain")
        self.assertEqual(out[1].text_type, TextType.TEXT)

    def test_text_node_with_no_links_is_kept(self):
        old_nodes = [TextNode("hello world", TextType.TEXT)]
        out = split_nodes_link(old_nodes)

        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].text, "hello world")
        self.assertEqual(out[0].text_type, TextType.TEXT)

    def test_single_link_middle(self):
        old_nodes = [TextNode("hi [a](u) bye", TextType.TEXT)]
        out = split_nodes_link(old_nodes)

        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in out],
            [
                ("hi ", TextType.TEXT, None),
                ("a", TextType.LINK, "u"),
                (" bye", TextType.TEXT, None),
            ],
        )

    def test_single_link_at_start(self):
        old_nodes = [TextNode("[a](u) end", TextType.TEXT)]
        out = split_nodes_link(old_nodes)

        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in out],
            [
                ("a", TextType.LINK, "u"),
                (" end", TextType.TEXT, None),
            ],
        )

    def test_single_link_at_end(self):
        old_nodes = [TextNode("start [a](u)", TextType.TEXT)]
        out = split_nodes_link(old_nodes)

        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in out],
            [
                ("start ", TextType.TEXT, None),
                ("a", TextType.LINK, "u"),
            ],
        )

    def test_multiple_links(self):
        old_nodes = [
            TextNode("x [a](u1) y [b](u2) z", TextType.TEXT)
        ]
        out = split_nodes_link(old_nodes)

        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in out],
            [
                ("x ", TextType.TEXT, None),
                ("a", TextType.LINK, "u1"),
                (" y ", TextType.TEXT, None),
                ("b", TextType.LINK, "u2"),
                (" z", TextType.TEXT, None),
            ],
        )


if __name__ == "__main__":
    unittest.main()