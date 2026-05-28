import sys
from textnode import TextNode

def main():
    textNode = TextNode("Some text", "link", "https://ww.be")
    return print(textNode)


if __name__ == "__main__":
    sys.exit(main())
