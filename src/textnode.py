import re

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
        nodes = TextNode.split_nodes_image(nodes)
        nodes = TextNode.split_nodes_link(nodes)
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

    def extract_markdown_images(text):
        return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    def extract_markdown_links(text):
        return re.findall(r"\[(.*?)\]\((.*?)\)", text)

    def split_nodes_image(old_nodes):
        new_nodes = []
        for node in old_nodes:
            images = TextNode.extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                text = node.text
                for image in images:
                    split = text.split(f"![{image[0]}]({image[1]})", 1)
                    if len(split[0]) > 0:
                        new_nodes.append(TextNode(split[0], "text"))
                    new_nodes.append(TextNode(image[0], "image", image[1]))
                    text = split[1]
                if len(text) > 0:
                    new_nodes.append(TextNode(text, "text"))
        return new_nodes

    def split_nodes_link(old_nodes):
        new_nodes = []
        for node in old_nodes:
            links = TextNode.extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                text = node.text
                for link in links:
                    split = text.split(f"[{link[0]}]({link[1]})", 1)
                    if len(split[0]) > 0:
                        new_nodes.append(TextNode(split[0], "text"))
                    new_nodes.append(TextNode(link[0], "link", link[1]))
                    text = split[1]
                if len(text) > 0:
                    new_nodes.append(TextNode(text, "text"))
        return new_nodes

    def markdown_to_blocks(markdown):
        blocks = markdown.split('\n')
        new_blocks = []
        current_block = ""
        for block in blocks:
            if block == "":
                if current_block != "":
                    new_blocks.append(current_block[:-1])
                    current_block = ""
            else:
                current_block += block.lstrip().rstrip() + "\n"
        if current_block != "":
            new_blocks.append(current_block[:-1])
        return new_blocks

    def block_to_block_type(block):
        count_h = 0
        while block[count_h] == '#':
            count_h += 1
        if count_h > 0 and count_h < 7 and block[count_h] == " ":
            return "header"

        if block[0:3] == "```" and block[-3:] == "```":
            return "code"

        quote = True
        unordered = True
        ordered = True
        item = 0
        for line in block.split("\n"):
            item += 1
            if line[0] != ">":
                quote = False
            if line[1] != " " or (line[0] != "*" and line[0] != "-"):
                unordered = False
            count = 0
            while line[count].isnumeric():
                count += 1

            ev = not line[0].isnumeric() or line[count] != "." or int(line[0:count]) != item
            if ev:
                ordered = False
        if quote:
            return "quote"
        if unordered:
            return "unordered_list"
        if ordered:
            return "ordered_list"

        return "paragraph"