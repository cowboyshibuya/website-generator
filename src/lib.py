from pydoc import html

from leafnode import LeafNode
from htmlnode import HTMLNode
from block import BlockType, block_to_block_type
from src.parentnode import ParentNode
from textnode import TextNode, TextType
import re

# take a raw markdown text and return a list of tuples
# each touple contain the alt text and the URL of any markdown image
# example: "This is a text with a ![rick roll](https://i.imgur.akhhfgjZ)" -> [("rick roll", "https://i.imgur.akhhfgjZ")]
def extract_markdown_image(text) :
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

# extract markdown links
# example: "this is a text with a link [test](https://www.test.com)" -> [("test", "https://www.test.com")]
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

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
            #print("parts :", parts)
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

    #print(nodes)
    return nodes

# takes a raw Makrdown string as input and returns a list of blocks string
def markdown_to_blocks(markdown):
    blocks = []
    # split string into blocks based on double newline
    parts = markdown.split("\n\n")

    for part in parts :
        if(part and len(part) > 0) :
            #print(part)
            # strip leading or trailing whitespace from each block
            cleaned_part = part.strip(" ")
            #print("cleaned : ", cleaned_part)
            blocks.append(cleaned_part.strip())

    #print("blocks :", blocks)
    return blocks

# convert a full markdown document into a single HTMLNode
def markdown_to_html_node(markdown) -> HTMLNode :
    # 1. split the markdown into blocks
    # 2. convert each block into an HTMLNode based on its type
    # 3. wrap all block nodes under a single parent div and return it
    blocks = markdown_to_blocks(markdown)
    block_nodes = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", block_nodes)

# dispatch a single block to the proper builder based on its type
def block_to_html_node(block) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    raise ValueError(f"invalid block type: {block_type}")

# a paragraph block: collapse its newlines into spaces, then inline-parse
def paragraph_to_html_node(block) -> HTMLNode:
    paragraph = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(paragraph))

# a code block is special: no inline markdown parsing of its content
def code_to_html_node(block) -> HTMLNode:
    text = block.strip("`")        # drop the ``` fences
    if text.startswith("\n"):
        text = text[1:]            # drop the single leading newline
    code = text_node_to_html_node(TextNode(text, TextType.code))
    return ParentNode("pre", [code])

# a heading block: count the leading "#" to pick h1-h6
def heading_to_html_node(block) -> HTMLNode:
    level = len(block) - len(block.lstrip("#"))
    text = block[level + 1:]       # skip the "#"* and the following space
    return ParentNode(f"h{level}", text_to_children(text))

# a quote block: strip the leading ">" from each line, join with a space
def quote_to_html_node(block) -> HTMLNode:
    lines = [line.lstrip(">").strip() for line in block.split("\n")]
    return ParentNode("blockquote", text_to_children(" ".join(lines)))

# an unordered list: each "- item" line becomes a <li>
def ulist_to_html_node(block) -> HTMLNode:
    items = [ParentNode("li", text_to_children(line[2:]))
             for line in block.split("\n")]
    return ParentNode("ul", items)

# an ordered list: strip the "N. " prefix from each line
def olist_to_html_node(block) -> HTMLNode:
    items = []
    for i, line in enumerate(block.split("\n")):
        text = line[len(f"{i + 1}. "):]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)

# takes a string of text and returns a list of HTMLNodes that represent the inline markdown
# using previously created functions (think TextNode -> HTMLNode).
def text_to_children(text) -> list[HTMLNode]:
    nodes : list[HTMLNode] = []
    textnodes = text_to_textnode(text)
    for node in textnodes :
        #print("node : ", node)
        leafnode = text_node_to_html_node(node)
        # htmlnode = leafnode.to_html()
        nodes.append(leafnode)
        #print("html node : ", htmlnode)

    return nodes
