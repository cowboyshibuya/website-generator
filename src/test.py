
import unittest

from lib import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_node_bold(self):
        node = TextNode("This is the best **day** of my life", TextType.text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        # print("response : ", new_nodes)
        self.assertEqual(new_nodes, [
            TextNode("This is the best ", TextType.text, None),
            TextNode("day", TextType.bold, None),
            TextNode(" of my life", TextType.text, None),
        ])

    def test_split_node_code(self):
        node = TextNode("This is a `python code` here", TextType.text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.text, None),
            TextNode("python code", TextType.code, None),
            TextNode(" here", TextType.text, None),
        ])
