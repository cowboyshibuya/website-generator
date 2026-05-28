from src.htmlnode import HTMLNode

# a leaf is a HTMLNode class that represents a single HTML tag with no children.
# for example : <p>Hello World</p> is a leaf.
# but <p> Hello, <b>World</b> </p> is not a leaf because it contains a children (<b>)
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = {}):
        super().__init__(self)
        self.value = value
        self.tag = tag
        self.props = props

    # render a leaf node as an HTML string (return string)
    # example:
        # LeafNode("p", "This is a paragraph of text.").to_html()
        # returns -> "<p>This is a paragraph of text.</p>"
    def to_html(self):
        if self.value == None:
            raise ValueError("No value")
        if self.tag == None:
            return self.value
        return f'<{self.tag}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode : {self.tag} {self.value} {self.props}"
