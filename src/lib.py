
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


# it takes a node list, a delimiter and a text type.
# it should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.
# for example:
    # node = TextNode("This is text with a `code block` word", TextType.TEXT)
    # new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
# should return :
    # [TextNode("This is a text with a ", TextType.Text), TextNode("code block", TextType.CODE), ...]
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list : list[TextNode] = []
    if text_type is TextType.text:
        new_list.extend(old_nodes)

    for node in old_nodes:
        split = node.text.split(delimiter)
        new_list.append(TextNode(split[0], TextType.text))
        new_node = TextNode(split[1], text_type)
        new_list.append(new_node)
        new_list.append(TextNode(split[2], TextType.text))

    return new_list
