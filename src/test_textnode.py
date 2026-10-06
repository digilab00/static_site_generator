import unittest
from textnode import *


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

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        compare_nodes = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("`code block`This is text with a `code block` word`code block`", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        compare_nodes = [
            TextNode("code block", TextType.CODE_TEXT),
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
         [
             TextNode("This is text with a link ", TextType.PLAIN_TEXT),
             TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
             TextNode(" and ", TextType.PLAIN_TEXT),
             TextNode(
                 "to youtube", TextType.LINK_TEXT, "https://www.youtube.com/@bootdotdev"
             ),
         ], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.PLAIN_TEXT),
                TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
            ]
            ,nodes)
        def test_extract_title_basic(self):
            md = "# Hello World"
            self.assertEqual(extract_title(md), "Hello World")
        
        def test_extract_title_multiline(self):
            md = "# Tolkien\nThis is paragraph content.\nAnother line."
            self.assertEqual(extract_title(md), "Tolkien")
    
        def test_extract_title_extra_whitespace(self):
            md = "#    Lots of Space Around Title    \nBody text"
            self.assertEqual(extract_title(md), "Lots of Space Around Title")
    
        def test_extract_title_empty_raises(self):
            md = ""
            with self.assertRaises(Exception):
                extract_title(md)
    
        def test_extract_title_no_text_after_hash_raises(self):
            md = "#   \nParagraph text"
            with self.assertRaises(Exception):
                extract_title(md)
if __name__ == "__main__":
    unittest.main()


