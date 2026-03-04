import unittest

from markdown_block import markdown_to_html_node, markdown_to_blocks, block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    # -------- paragraphs --------
    def test_paragraph_single_line(self):
        block = "hello world"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline_is_still_paragraph(self):
        block = "hello\nworld"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # -------- headings --------
    def test_heading_h1(self):
        block = "# Title"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### Title"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    # -------- code --------
    def test_code_block(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    # -------- quote --------
    def test_quote_block(self):
        block = "> hello\n> world"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    # -------- unordered list (updated spec: '-' and '*' allowed) --------
    def test_unordered_list_dash(self):
        block = "- a\n- b\n- c"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_star(self):
        block = "* a\n* b"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_mixed_dash_star(self):
        block = "- a\n* b\n- c"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    # -------- ordered list --------
    def test_ordered_list_strict_numbering(self):
        block = "1. a\n2. b\n3. c"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_second_line_becomes_paragraph(self):
        # Because the ordered-list check requires "2. " exactly.
        block = "1. ok\n2) nope"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_number_sequence_becomes_paragraph(self):
        block = "1. a\n3. b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def assertHtmlEqual(self, actual: str, expected: str):
        self.assertEqual(actual, expected)

    # -------- base cases --------
    def test_empty_markdown_returns_empty_div(self):
        node = markdown_to_html_node("")
        self.assertHtmlEqual(node.to_html(), "<div></div>")

    def test_whitespace_only_markdown_returns_empty_div(self):
        node = markdown_to_html_node("   \n\n  \n")
        self.assertHtmlEqual(node.to_html(), "<div></div>")

    # -------- paragraph rendering --------
    def test_paragraph_wraps_in_p_and_joins_newlines_with_space(self):
        md = "Hello\nworld"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(node.to_html(), "<div><p>Hello world</p></div>")

    def test_multiple_paragraph_blocks(self):
        md = "First paragraph.\nStill first.\n\nSecond paragraph."
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(
            node.to_html(),
            "<div><p>First paragraph. Still first.</p><p>Second paragraph.</p></div>",
        )

    # -------- headings --------
    def test_heading_h1(self):
        md = "# Title"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(node.to_html(), "<div><h1>Title</h1></div>")

    def test_heading_h3(self):
        md = "### Smaller title"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(node.to_html(), "<div><h3>Smaller title</h3></div>")

    def test_heading_with_inline_formatting_survives(self):
        md = "## Hello **bold** and _italics_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertTrue(html.startswith("<div><h2>"))
        self.assertIn("<b>bold</b>", html)     # change to <strong> if your renderer uses that
        self.assertIn("<i>italics</i>", html)  # change to <em> if your renderer uses that
        self.assertTrue(html.endswith("</h2></div>"))

    # -------- code blocks --------
    def test_code_block_renders_pre_code(self):
        md = "```\nprint('hi')\n```"
        node = markdown_to_html_node(md)

        # Your implementation uses cleaned_code = block[3:-3]
        # so it preserves interior newlines exactly as sliced.
        self.assertHtmlEqual(
            node.to_html(),
            "<div><pre><code>\nprint('hi')\n</code></pre></div>",
        )

    def test_code_block_does_not_parse_inline_markdown(self):
        md = "```\nthis is **not bold**\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("**not bold**", html)
        self.assertNotIn("<b>", html)
        self.assertNotIn("<strong>", html)

    # -------- quotes --------
    def test_blockquote_strips_leading_gt_and_joins_lines(self):
        md = "> hello\n> world"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(
            node.to_html(),
            "<div><blockquote>hello world</blockquote></div>",
        )

    def test_blockquote_allows_mixed_spacing_after_gt(self):
        md = ">hello\n>   world"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(
            node.to_html(),
            "<div><blockquote>hello world</blockquote></div>",
        )

    def test_blockquote_with_inline_formatting_survives(self):
        md = "> hi **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<blockquote>", html)
        self.assertIn("<b>bold</b>", html)  # change to <strong> if needed

    # -------- unordered lists (updated spec: '-' and '*' allowed) --------
    def test_unordered_list_dash_items(self):
        md = "- a\n- b\n- c"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(
            node.to_html(),
            "<div><ul><li>a</li><li>b</li><li>c</li></ul></div>",
        )

    def test_unordered_list_star_items(self):
        md = "* a\n* b"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(
            node.to_html(),
            "<div><ul><li>a</li><li>b</li></ul></div>",
        )

    def test_unordered_list_mixed_symbols_renders_correctly(self):
        md = "- a\n* b\n- c"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(
            node.to_html(),
            "<div><ul><li>a</li><li>b</li><li>c</li></ul></div>",
        )

    def test_unordered_list_inline_formatting_in_items(self):
        md = "- hello **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<ul>", html)
        self.assertIn("<li>hello <b>bold</b></li>", html)  # change to <strong> if needed

    # -------- ordered lists --------
    def test_ordered_list_basic(self):
        md = "1. a\n2. b\n3. c"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(
            node.to_html(),
            "<div><ol><li>a</li><li>b</li><li>c</li></ol></div>",
        )

    def test_ordered_list_inline_formatting_in_items(self):
        md = "1. hello _italics_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<ol>", html)
        self.assertIn("<li>hello <i>italics</i></li>", html)  # change to <em> if needed

    def test_bad_ordered_list_format_currently_renders_as_paragraph(self):
        # Current behavior: not ORDERED_LIST => paragraph, so no exception raised.
        md = "1. ok\n2) nope"
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(node.to_html(), "<div><p>1. ok 2) nope</p></div>")

    # -------- mixed document integration --------
    def test_mixed_blocks_render_in_correct_order(self):
        md = "\n\n".join(
            [
                "# Title",
                "A paragraph\nwith two lines.",
                "> a quote\n> with two lines",
                "- uno\n* dos",
                "1. first\n2. second",
                "```\ncode\n```",
            ]
        )
        node = markdown_to_html_node(md)
        self.assertHtmlEqual(
            node.to_html(),
            "<div>"
            "<h1>Title</h1>"
            "<p>A paragraph with two lines.</p>"
            "<blockquote>a quote with two lines</blockquote>"
            "<ul><li>uno</li><li>dos</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "<pre><code>\ncode\n</code></pre>"
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()