import unittest

from lib import text_node_to_html_node
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.italic)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.bold, "http://test.com")
        node2 = TextNode("This is a text node", TextType.bold, "http://test.com")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.bold, "http://test.com")
        node2 = TextNode("This is a text node", TextType.bold, "http://test2.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("this is a text node", TextType.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "this is a text node")

if __name__ == "__main__":
    unittest.main()
