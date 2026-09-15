import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a temxt node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        example = f'TextNode({node.text}, {node.text_type}, {node.url})'
        self.assertEqual(node.__repr__(), example)

    def test_null_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        if node.url == None:
            return True

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        self.assertNotEqual(node.text_type, node2.text_type)
        
if __name__ == "__main__":
    unittest.main()