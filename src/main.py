from textnode import TextNode
from htmlnode import (HTMLNode, LeafNode, ParentNode)
import os
import shutil

def main():
    #test_text_to_nodes()
    #test_extract()
    #test_images()
    #test_blocks()
    #test_block_types()
    #test_html_node()

    copy_folder("static", "public")
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

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
    title = extract_title(text)
    print(f"Title: {title}")
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
            
def text_to_html(text):
    blocks = TextNode.markdown_to_blocks(text)
    html_text = ""
    for block in blocks:
        block_type = TextNode.block_to_block_type(block)
        html = None
        if block_type == "paragraph":
            html = html_node(block, "p")
        elif block_type == "quote":
            html = html_quote(block)
        elif block_type == "unordered_list":
            html = html_list_node(block, "ul")
        elif block_type == "ordered_list":
            html = html_list_node(block, "ol")
        elif block_type == "header":
            html = html_node_heading(block)
        if html:
            html_text += html.to_html()
    return html_text

def html_node(block, tag):
    leafs = []
    for node in TextNode.text_to_nodes(block):
        leafs.append(HTMLNode.text_node_to_html_node(node))
    parent = ParentNode(tag, leafs)
    return parent

def html_quote(block):
    leafs = []
    for line in block.split("\n"):
        stripped_line = line[1:].lstrip() + " "
        for node in TextNode.text_to_nodes(stripped_line):
            leafs.append(HTMLNode.text_node_to_html_node(node))
    parent = ParentNode("blockquote", leafs)
    return parent

def html_list_node(block, tag):
    leafs = []
    for line in block.split("\n"):
        if tag == "ul":
            line = line[1:]
        if tag == "ol":
            count = 0
            while block[count].isnumeric():
                count += 1
            line = line[count + 2:]
        list_item = html_node(line, "li")
        leafs.append(list_item)
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

def copy_folder(from_folder, to_folder):
    if not os.path.exists(from_folder):
        print(f"folder {from_folder} doesn't exist")
        return

    if os.path.exists(to_folder):
        print(f"removing folder {to_folder}")
        shutil.rmtree(to_folder)
    print(f"creating folder {to_folder}")
    os.mkdir(to_folder)

    for path in os.listdir(from_folder):
        old_path = os.path.join(from_folder, path)
        new_path = os.path.join(to_folder, path)
        if os.path.isfile(old_path):            
            print(f"copying form {old_path} to {new_path}")
            shutil.copy(old_path, new_path)
        else:
            copy_folder(old_path, new_path)

def extract_title(markdown):
    for line in markdown.split("\n"):
        stripped_line = line.lstrip()
        if len(stripped_line) > 1 and stripped_line[0] == "#" and stripped_line[1] != "#":
            return stripped_line[1:].lstrip()
    raise ValueError("markdown has no h1 heading")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    html = text_to_html(markdown)
    title = extract_title(markdown)
    html_file = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    with open(dest_path, "w") as file:
        file.write(html_file)
    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_content):
    print(f"looking for md files in {dir_path_content}")
    if not os.path.exists(dest_dir_content):
        os.mkdir(dest_dir_content)

    for path in os.listdir(dir_path_content):
        old_path = os.path.join(dir_path_content, path)
        new_path = os.path.join(dest_dir_content, path)
        if os.path.isfile(old_path) and old_path[-3:] == ".md":
            new_path = new_path[:-3] + ".html"
            generate_page(old_path, template_path, new_path)
        else:
            generate_pages_recursive(old_path, template_path, new_path)

        



main()