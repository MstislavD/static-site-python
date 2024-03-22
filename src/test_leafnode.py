import unittest

from htmlnode import LeafNode, ParentNode

class LeafNodeTest(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("a", "Click me!", {("href", "https://www.google.com")})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        node = LeafNode("p", "This is a paragraph of text")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text</p>")

class ParentNodeTest(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()