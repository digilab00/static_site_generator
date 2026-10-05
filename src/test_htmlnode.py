import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_value_error(self):
        node = LeafNode(None, None, None)
        self.assertRaises(ValueError)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )