class TextNode:
    type_by_delimeter = {
            "**" : "bold",
            "*" : "italic",
            "`" : "code"
        }

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_to_nodes(text):
        node = TextNode(text, "text")
        nodes = TextNode.split_nodes_delimeter([node], "**", "text")
        nodes = TextNode.split_nodes_delimeter(nodes, "*", "text")
        nodes = TextNode.split_nodes_delimeter(nodes, "`", "text")
        return nodes

    def split_nodes_delimeter(old_nodes, delimeter, text_type):
        new_nodes = []
        for node in old_nodes:
            if node.text_type == "text":
                n_s = node.text.split(delimeter)
                for i in range(0, len(n_s)):
                    if len(n_s[i]) == 0:
                        continue
                    if i % 2 == 0:
                        new_nodes.append(TextNode(n_s[i], "text"))
                    else:
                        new_nodes.append(TextNode(n_s[i], TextNode.type_by_delimeter[delimeter]))
            else:
                new_nodes.append(node)
        return new_nodes