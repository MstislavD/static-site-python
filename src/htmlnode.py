from textnode import TextNode

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_list = []
        for prop in self.props:
            prop_list.append(f"{prop[0]}=\"{prop[1]}\" ")
        prop_list.sort()
        prop_string =""
        for prop in prop_list:
            prop_string += prop
        return prop_string[:-1]

    def text_node_to_html_node(text_node):
        if (text_node.text_type == "text"):
            return LeafNode(None, text_node.text)
        if (text_node.text_type == "bold"):
            return LeafNode("b", text_node.text)
        if (text_node.text_type == "italic"):
            return LeafNode("i", text_node.text)
        if (text_node.text_type == "code"):
            return LeafNode("code", text_node.text)
        if (text_node.text_type == "link"):
            return LeafNode("a", text_node.text, {("href", text_node.url)})
        if (text_node.text_type == "image"):
            return LeafNode("img", "", {("src", text_node.url), ("alt", text_node.text)})


    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Value not provided")
        if not self.tag:
            return f"{self.value}"
        if self.tag == "a":
            for prop in self.props:
                if prop[0] == "href":
                    return f"<a {super().props_to_html()}>{self.value}</a>"
        if self.tag == "b" or self.tag == "i" or self.tag == "p" or self.tag == "code" or self.tag == "li":
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return "Error!"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag not provided")
        if len(self.children) == 0:
            raise ValueError("Node has no children")
        text = f"<{self.tag}>"
        for child in self.children:
            text += child.to_html()
        text += f"</{self.tag}>"
        return text

