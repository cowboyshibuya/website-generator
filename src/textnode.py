from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    text = ""
    bold = "**"
    italic = "_"
    code = "`"
    link = "["
    image = "!["

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url or None

    def __eq__(self, other):
        # if other is not a TextNode object
        if not isinstance(other, TextNode):
            return False

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


# bridge a single TextNode into its LeafNode (HTML) representation
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
