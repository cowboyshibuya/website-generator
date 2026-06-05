from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag = tag, value=None, children=children, props=props)
        self.tag = tag
        self.children = children
        self.props = props or {}

    # we will implement a recursive method to generate each
    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag")
        if self.children is None:
            raise ValueError("no children")

        # will join all children html method
        childrenHtml = "".join(child.to_html() for child in self.children)

        return f'<{self.tag}>{childrenHtml}</{self.tag}>'
