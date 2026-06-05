import re

from textnode import TextNode, TextType

# take a raw markdown text and return a list of tuples
# each touple contain the alt text and the URL of any markdown image
# example: "This is a text with a ![rick roll](https://i.imgur.akhhfgjZ)" -> [("rick roll", "https://i.imgur.akhhfgjZ")]
def extract_markdown_image(text) :
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

# extract markdown links
# example: "this is a text with a link [test](https://www.test.com)" -> [("test", "https://www.test.com")]
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

# it takes a node list, a delimiter and a text type.
# it should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.
# for example:
    # node = TextNode("This is text with a `code block` word", TextType.TEXT)
    # new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
# should return :
    # [TextNode("This is a text with a ", TextType.Text), TextNode("code block", TextType.CODE), ...]
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes : list[TextNode] = []

    for node in old_nodes:
        # if already text type -> not process again
        if node.text_type is not TextType.text:
            new_nodes.append(node)
            continue

        # we split into parts to have a BEFORE and AFTER the delimiter
        parts = node.text.split(delimiter)
        # the even part will always be TEXT type (parts[0], parts[2])

        # the parts should always be ODD if a node correctly contains a Type
        # for example: "Hello, this is "
        if len(parts) % 2 == 0:
            raise ValueError("unmatch delimiter : ", delimiter)

        for index, part in enumerate(parts):
            if not part:
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(part, TextType.text))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

# "This is a text with a ![image](https://image.com) and another ![image](https://image2.com)"
# -> [TextNode("This is a text with a ", TextType.text), TextNode("image", TextType.image, "https://image.com"), TextNode(" and another", TextType.text), TextNode("image", TextType.image, "https://image2.com")]
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes : list[TextNode] = []

    for node in old_nodes:
        if node.text_type is not TextType.text:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        images = extract_markdown_image(node.text)

        if not images:
            new_nodes.append(node)
            continue

        for image_alt, image_link in images:
            parts = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.text))

            new_nodes.append(TextNode(f"{image_alt}", TextType.image, f"{image_link}"))
            remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.text))
    return new_nodes

def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes : list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.text:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue

        for link_text, link_url in links:
            parts = remaining_text.split(f"[{link_text}]({link_url})", 1)
            if parts[0] :
                new_nodes.append(TextNode(parts[0], TextType.text))

            new_nodes.append(TextNode(f"{link_text}", TextType.link, f"{link_url}"))
            remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.text))
    return new_nodes

# convert a raw string of markdown text into a list of TextNode objects
# example : "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
# -> [TextNode("this is ", TextNode.text), TextNode("text", TextType.bold), ...]
def text_to_textnode(text) -> list[TextNode] :
    nodes = [TextNode(text, TextType.text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.bold)
    nodes = split_nodes_delimiter(nodes, "_", TextType.italic)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)

    return nodes
