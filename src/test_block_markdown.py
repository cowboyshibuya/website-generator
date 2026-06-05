import textwrap
import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlockToBlockType(unittest.TestCase):
    def test_unordored_list_block(self):
        block = "- This is a list\n- with items"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_ordererd_list_block(self):
        block = "1. This is a list\n2. with items"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_heading_block(self):
        block = "# This is a heading 1"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_paragraph_heading(self):
        block = "#This is a wrong heading1"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))


class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """)

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = textwrap.dedent("""
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = textwrap.dedent("""
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
