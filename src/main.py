from textnode import TextNode

def main():
    text = "This is **bold** text, and this is *italic* text, and finally a `code` text"
    text2 = "**BOLD** text"
    nodes = TextNode.text_to_nodes(text2)
    for n in nodes:
        print(n)

main()