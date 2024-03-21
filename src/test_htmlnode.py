import unittest

from htmlnode import HTMLNode

class HTMLNodeTest(unittest.TestCase):
    def test_eq(self):
        props = {
            ("prop1", "first prop"),
            ("prop2", "second prop")
        }
        node = HTMLNode(props=props)
        self.assertEqual("prop1=first prop prop2=second prop", node.props_to_html())

if __name__ == "__main__":
    unittest.main()