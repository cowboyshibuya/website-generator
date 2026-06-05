from enum import Enum

from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnode


class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDERED_LIST = "unordered_list",
    ORDERED_LIST = "ordered_list"

# takes a block and returns a Block Type
def block_to_block_type(block : str) -> BlockType :
    # HEADING: check if starts with 1-6 "#" followed by a white space
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")) :
        return BlockType.HEADING

    # CODE
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # QUOTE
    if block.startswith(("> ", ">")) :
        return BlockType.QUOTE

    # UNORDERED LIST
    if block.startswith("- "):
        return BlockType.UNORDERED_LIST

    # ORDERED LIST
    lines = block.split("\n")
    i = 1
    for line in lines:
        if not line.startswith(f"{i}. "):
            continue
        i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

# takes a raw Markdown string as input and returns a list of block strings
def markdown_to_blocks(markdown):
    blocks = []
    # split string into blocks based on double newline
    parts = markdown.split("\n\n")

    for part in parts :
        if(part and len(part) > 0) :
            # strip leading or trailing whitespace from each block
            cleaned_part = part.strip(" ")
            blocks.append(cleaned_part.strip())

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
        leafnode = text_node_to_html_node(node)
        nodes.append(leafnode)

    return nodes
