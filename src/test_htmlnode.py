import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_not_eq(self):
        node = HTMLNode()
        node2 = HTMLNode('garb')
        self.assertNotEqual

    def test_repr(self):
        node = HTMLNode()
        example = f'HTMLNode(f{node.tag}, f{node.value}, f{node.children}, f{node.props})'
        self.assertEqual(node.__repr__(), example)

    def test_null(self):
        node = HTMLNode()
        if node.children == None and node.props == None and node.tag == None and node.value == None:
            return True
        return False
    