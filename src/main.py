from textnode import TextNode
from htmlnode import (HTMLNode, LeafNode, ParentNode)

def main():
    #test_text_to_nodes()
    #test_extract()
    #test_images()
    #test_blocks()
    #test_block_types()
    test_html_node()

def test_text_to_nodes():
    text = "This is **bold** text, and this is *italic* text, and finally a `code` text"
    text2 = "**BOLD** text"
    text3 = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
    nodes = TextNode.text_to_nodes(text3)
    for n in nodes:
        print(n)

def test_extract():
    text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
    print(TextNode.extract_markdown_images(text))
    # [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/dfsdkjfd.png")]

    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    print(TextNode.extract_markdown_links(text))
    # [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]

def test_images():
    text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
    node = TextNode(text, "text")
    nodes = TextNode.split_nodes_image([node])
    for n in nodes:
        print(n)

def test_blocks():
    text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line   

* This is a list
* with items"""
    blocks = TextNode.markdown_to_blocks(text)
    count = 1
    for block in blocks:
        print(count)
        print(block)
        count += 1

def test_block_types():
    text = []
    # text.append("# header")
    # text.append("### header")
    # text.append("###### header")
    # text.append("#_not header")
    # text.append("######## not header")
    # text.append("``` code ```")
    # text.append("``` not code")
    # text.append("> quote line\n> second quote line")
    # text.append("> quote line\nnot quote line\n> quote line")
    # text.append("* item\n* item\n- item")
    # text.append("* item\n** not item\n- item")
    # text.append("* item\nnot item\n* item")
    text.append("1. item\n2. item\n3. item")
    text.append("1. item\n3. item")
    text.append("1. item\n2 item")

    for t in text:
        print(f"{t}\nType: {TextNode.block_to_block_type(t)}\n")

def test_html_node():
    text = "This is **bold** text, and this is *italic* text, and finally a `code` text"
    text += "\n\n# heading"
    text += "\n\n## heading with a [link](https://www.example.com)"
    text += "\n\n###### heading with **bold** and **italic** text"
    text += "\n\n> quote line 1\n> quote line 2\n> quote **line 3**"
    text += "\n\n* item\n* item"
    text += "\n\n1. item\n2. item\n 3. item"
    blocks = TextNode.markdown_to_blocks(text)
    for block in blocks:
        block_type = TextNode.block_to_block_type(block)
        html = None
        if block_type == "paragraph":
            html = html_node(block, "p")
        elif block_type == "quote":
            html = html_node(block, "blockquote")
        elif block_type == "unordered_list":
            html = html_list_node(block, "ul")
        elif block_type == "ordered_list":
            html = html_list_node(block, "ol")
        elif block_type == "header":
            html = html_node_heading(block)
        if html:
            print(html.to_html())

def html_node(block, tag):
    leafs = []
    for node in TextNode.text_to_nodes(block):
        leafs.append(HTMLNode.text_node_to_html_node(node))
    parent = ParentNode(tag, leafs)
    return parent

def html_list_node(block, tag):
    leafs = []
    for line in block.split("\n"):
        node = LeafNode("li", line)
        leafs.append(node)
    parent = ParentNode(tag, leafs)
    return parent

def html_node_heading(block):
    leafs = []
    count = 0
    while block[count] == "#":
        count += 1
    block = block[count:].lstrip()
    tag = f"h{count}"
    return html_node(block, tag)

main()