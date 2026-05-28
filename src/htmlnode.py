class HTMLNode:
    def __init__(
        self,
        tag = None,
        value = None,
        children = None,
        props = {}
    ):
        self.tag = tag # string to represent HTML tag ("p", "a", "h1", etc.)
        self.value = value # string to represent HTML value (text inside the tag)
        self.children = children # a HTMLNode object to represent children of the node
        self.props = props # dict of key-value representing the attributes of the HTML tag ("href : ...", etc.)

    def to_html(self):
        raise NotImplementedError()

    # convert props to html. for example :
        # { "href" : "https://www.google.com", "target" : "_blank"}
        # will return -> href="https://www.google.com" target="_blank"
    def props_to_html(self):
        # return " ".join(map(str,self.props.values()))
        return " ".join(
            f'{key}="{value}"'
            for key, value in self.props.items()
        )

    def __repr__(self):
        return f"HTMLNode : {self.tag} {self.value} {self.children} {self.props}"
