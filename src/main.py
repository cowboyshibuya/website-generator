import sys
from generate_page import generate_page, generate_pages_recursive
from textnode import TextNode
from cp_source_to_destination import cp_source_to_destination
def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    cp_source_to_destination("./static", "./docs")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

if __name__ == "__main__":
    sys.exit(main())
