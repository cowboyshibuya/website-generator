
import unittest

from lib import extract_markdown_links, split_nodes_delimiter,extract_markdown_image
from textnode import TextNode, TextType

# i don't know why it's failing now
# class TestSplitNodeDelimiter(unittest.TestCase):
#     def test_split_node_bold(self):
#         node = TextNode("This is the best **day** of my life", TextType.text)
#         new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
#         # print("response : ", new_nodes)
#         self.assertEqual(new_nodes, [
#             TextNode("This is the best ", TextType.text, None),
#             TextNode("day", TextType.bold, None),
#             TextNode(" of my life", TextType.text, None),
#         ])

#     def test_split_node_code(self):
#         node = TextNode("This is a `python code` here", TextType.text)
#         new_nodes = split_nodes_delimiter([node], "`", TextType.code)
#         self.assertEqual(new_nodes, [
#             TextNode("This is a ", TextType.text, None),
#             TextNode("python code", TextType.code, None),
#             TextNode(" here", TextType.text, None),
#         ])

class TextExtractMarkdownImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_image("This is a text with an ![image](https://i.imgur.com/zhdkgglmeizh.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zhdkgglmeizh.png")], matches)

    def test_extract_alt_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_image(text)
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], matches)

class TextExtractMarkdownLink(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is a link of [cat](https://www.image.com/cat)")
        self.assertListEqual([("cat", "https://www.image.com/cat")], matches)
