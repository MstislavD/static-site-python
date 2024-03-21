class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string =""
        for prop in self.props:
            prop_string += f"{prop[0]}={prop[1]} "
        return prop_string[:-1]

    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"
