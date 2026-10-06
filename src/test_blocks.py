import unittest
from textnode import *
from htmlnode import *
from blocks import *

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_false_positives(self):
        # 7 hashes is not a heading (only 1-6 allowed)
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
        # Missing space after hash
        self.assertEqual(block_to_block_type("#Not a heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ndef hello():\n    return 'world'\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_invalid(self):
        # Missing newline after opening backticks
        block = "```python\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        # Missing closing backticks
        block_unclosed = "```\nprint('hi')"
        self.assertEqual(block_to_block_type(block_unclosed), BlockType.PARAGRAPH)

    def test_quote_block(self):
        # Tests quotes both with and without space after '>'
        block = ">First quote line\n> Second quote line\n>Third quote line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_invalid(self):
        # One line is missing '>'
        block = "> First line\nSecond line without quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid(self):
        # Missing space after '-'
        block = "-item 1\n-item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        # One line missing bullet
        block_mixed = "- item 1\nitem 2"
        self.assertEqual(block_to_block_type(block_mixed), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid(self):
        block_starts_at_two = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(block_starts_at_two), BlockType.PARAGRAPH)
        block_skipped_number = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block_skipped_number), BlockType.PARAGRAPH)
        block_missing_space = "1.First\n2.Second"
        self.assertEqual(block_to_block_type(block_missing_space), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "This is a simple paragraph block with some normal text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_markdown_to_html_node_paragraph(self):
            md = "This is a simple paragraph with **bold** and _italic_ text."
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is a simple paragraph with <b>bold</b> and <i>italic</i> text.</p></div>",
            )

    def test_markdown_to_html_node_headings(self):
        md = """# Heading 1

### Heading 3 with **bold**"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h3>Heading 3 with <b>bold</b></h3></div>",
        )

    def test_markdown_to_html_node_code_block(self):
        md = "```\ndef hello():\n    return 'world'\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>def hello():\n    return 'world'\n</code></pre></div>",
        )

    def test_markdown_to_html_node_quote(self):
        md = """> Quote line 1
> Quote line 2 with **bold**"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote line 1 Quote line 2 with <b>bold</b></blockquote></div>",
        )

    def test_markdown_to_html_node_unordered_list(self):
        md = """- First item
- Second item with `code`
- Third item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <code>code</code></li><li>Third item</li></ul></div>",
        )

    def test_markdown_to_html_node_ordered_list(self):
        md = """1. First step
2. Second step with _italics_
3. Third step"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First step</li><li>Second step with <i>italics</i></li><li>Third step</li></ol></div>",
        )

    def test_markdown_to_html_node_multiblock(self):
        md = """# Document Title

This is an introductory paragraph.

- Item A
- Item B

> Final concluding quote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Document Title</h1><p>This is an introductory paragraph.</p><ul><li>Item A</li><li>Item B</li></ul><blockquote>Final concluding quote</blockquote></div>",
        )