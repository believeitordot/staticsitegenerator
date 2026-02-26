import unittest

from textnode import TextType, TextNode
from markdown_inline import extract_markdown_images, extract_markdown_links, split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_no_closing_delimiter(self):
        node = TextNode("This is text with **incorrect markdown syntax", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_delimiter_at_the_beginning(self):
        node = TextNode("**This is** text with correct markdown syntax", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = [
            TextNode("This is", TextType.BOLD),
            TextNode(" text with correct markdown syntax", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, result)
    
    def test_split_delimiter_at_the_end(self):
        node = TextNode("This is text with correct _markdown syntax_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result = [
            TextNode("This is text with correct ", TextType.TEXT),
            TextNode("markdown syntax", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_with_multiple_delimiters(self):
        node = TextNode("This is _text with_ correct _markdown syntax_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text with", TextType.ITALIC),
            TextNode(" correct ", TextType.TEXT),
            TextNode("markdown syntax", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, result)