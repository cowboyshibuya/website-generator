from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDERED_LIST = "unordered_list",
    ORDERED_LIST = "ordered_list"

# takes a block and returns a Block Type
def block_to_block_type(block : str) -> BlockType :

    print("block : ", block)
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
