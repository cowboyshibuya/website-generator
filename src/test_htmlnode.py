import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(None, None, None, {"href" : "https://www.google.com", "target" : "_blank"})
        response = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), response)
