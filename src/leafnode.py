from src.htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value, tag):
        #super().__init__(self)
        self.value = value
        self.tag = tag

    # render a leaf node as an HTML string (return string)
    # example:
        # LeafNode("p", "This is a paragraph of text.").to_html()
        # returns -> "<p>This is a paragraph of text.</p>"
    def to_html(self):
        if self.value == None:
            raise ValueError("No value")
        if self.tag == None:
            return self.value

       return (f"<{self.tag}>{self.value}</{self.tag}>")
