import unittest

from block import BlockType, block_to_block_type

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
