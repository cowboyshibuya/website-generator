import sys
from generate_page import generate_page
from textnode import TextNode
from cp_source_to_destination import cp_source_to_destination
def main():
    # textNode = TextNode("Some text", "link", "https://ww.be")
    # return print(textNode)

    # copy files from "static" to "public"
    cp_source_to_destination("./static", "./public")
    # generate a page from "content/index.md" using "template.html" and write it to "public/index.html"
    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    sys.exit(main())
