import unittest
from htmlnode import HTMLNode, LeafNode

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

    def test_props_to_html(self):
        props = {'key':'value','key2':'value2'}
        node = HTMLNode(props=props)
        assert node.props_to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")