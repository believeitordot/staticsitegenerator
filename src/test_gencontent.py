import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_simple_h1(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_h1_not_first_line(self):
        markdown = "Some intro text\n# Real Title\nMore text"
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_multiple_h1_returns_first(self):
        markdown = "# First Title\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_ignores_h2(self):
        markdown = "## Subtitle\n# Real Title"
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_ignores_hash_without_space(self):
        markdown = "#Title\n# Valid Title"
        self.assertEqual(extract_title(markdown), "Valid Title")

    def test_leading_space_invalid(self):
        markdown = " # Not valid\n# Valid"
        self.assertEqual(extract_title(markdown), "Valid")

    def test_raises_when_no_h1(self):
        markdown = "No headers here\n## Just h2"
        with self.assertRaises(ValueError)::
            extract_title(markdown)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")