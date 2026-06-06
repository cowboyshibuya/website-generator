import sys
from textnode import TextNode
from cp_source_to_destination import cp_source_to_destination
def main():
    # textNode = TextNode("Some text", "link", "https://ww.be")
    # return print(textNode)
    cp_source_to_destination("./static", "./public")


if __name__ == "__main__":
    sys.exit(main())
