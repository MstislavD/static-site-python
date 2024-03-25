from textnode import TextNode

def main():
    test_text_to_nodes()
    #test_extract()
    #test_images()

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

main()