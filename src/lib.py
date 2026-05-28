
# convert a TextNode to an HTMLNode (specifically a LeafNode)
from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    type = text_node.text_type
    text = text_node.text

    if not isinstance(type, TextType):
        raise Exception("invalid text type")
    if type is TextType.text:
        return LeafNode(None, text)
    if type is TextType.bold:
        return LeafNode("b", text)
    if type is TextType.italic:
        return LeafNode("i", text)
    if type is TextType.code:
        return LeafNode("code", text)
    if type is TextType.link:
        return LeafNode("a", text, {"href" : text_node.url})
    if type is TextType.image:
        return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})

    raise Exception("invalid text type")
