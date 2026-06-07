import textwrap
import unittest

from inline_markdown import (
    extract_markdown_image,
    extract_markdown_links,
    extract_title,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_links,
    text_to_textnode,
)
from textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_node_bold(self):
        node = TextNode("This is the best **day** of my life", TextType.text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
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

class TestExtractMarkdownImage(unittest.TestCase):
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

class TestExtractMarkdownLink(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is a link of [cat](https://www.image.com/cat)")
        self.assertListEqual([("cat", "https://www.image.com/cat")], matches)

class TextSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode("This is a text with a link [to my website](https://example.com) and [to my youtube channel](https://youtube.com)", TextType.text)
        matches = split_nodes_links([node])
        self.assertListEqual([
            TextNode("This is a text with a link ", TextType.text),
            TextNode("to my website", TextType.link, "https://example.com"),
            TextNode(" and ", TextType.text),
            TextNode("to my youtube channel", TextType.link, "https://youtube.com")
        ], matches)

class TextSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode("This is a text with a ![image](https://image.com) and another ![image](https://image2.com)", TextType.text)
        matches = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is a text with a ", TextType.text),
            TextNode("image", TextType.image, "https://image.com"),
            TextNode(" and another ", TextType.text),
            TextNode("image", TextType.image, "https://image2.com")
        ], matches)

    def test_split_image_without_image(self):
        node = TextNode("plain text only", TextType.text)
        self.assertListEqual(
            [TextNode("plain text only", TextType.text)],
            split_nodes_image([node])
        )

    def test_split_image_at_start(self):
        node = TextNode("![cat](cat.png) after", TextType.text)
        self.assertListEqual([
            TextNode("cat", TextType.image, "cat.png"),
            TextNode(" after", TextType.text),
        ], split_nodes_image([node]))

    def test_split_image_at_end(self):
        node = TextNode("before ![cat](cat.png)", TextType.text)
        self.assertListEqual([
            TextNode("before ", TextType.text),
            TextNode("cat", TextType.image, "cat.png"),
        ], split_nodes_image([node]))

    def test_preserves_non_text_nodes(self):
        node = TextNode("already bold text", TextType.bold)
        self.assertListEqual(
            [node],
            split_nodes_image([node])
        )


class TestTextToTextNode(unittest.TestCase):
    def test_bold_code_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual([
            TextNode("This is ", TextType.text),
            TextNode("text", TextType.bold),
            TextNode(" with an ", TextType.text),
            TextNode("italic", TextType.italic),
            TextNode(" word and a ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" and an ", TextType.text),
            TextNode("obi wan image", TextType.image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.text),
            TextNode("link", TextType.link, "https://boot.dev"),
        ], text_to_textnode(text))

class TestExtractTitle(unittest.TestCase):
    def test_extract_correct_h1(self):
        text = "# Hello World"
        self.assertEqual("Hello World", extract_title(text))

    def test_extract_h1_with_spaces(self):
        text = "# Hello World       "
        self.assertEqual("Hello World", extract_title(text))

    def test_extract_h1_multilines(self):
        text = textwrap.dedent("""# Hello World
            ![ksjf](images.com)
            This is wonderful
        """)
        self.assertEqual("Hello World", extract_title(text))

if __name__ == "__main__":
    unittest.main()
