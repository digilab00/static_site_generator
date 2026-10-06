from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
import re

class TextType(Enum):
    PLAIN_TEXT = 'plain'
    BOLD_TEXT = 'bold'
    ITALIC_TEXT = 'italic'
    CODE_TEXT = 'code'
    LINK_TEXT = 'link'
    IMAGES = 'images'

class TextNode:
    def __init__(self, text, type, url: str | None = None):
        self.text: str = text
        self.text_type: TextType = type
        self.url = url
        
    def __eq__(self, node: TextNode):
        return (self.text, self.text_type, self.url) == (node.text, node.text_type, node.url)
            
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode('i', text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode('code', text_node.text)
        case TextType.LINK_TEXT:
            props = {'href':text_node.url}
            return LeafNode('a', text_node.text, props)
        case TextType.IMAGES:
            props = {
                'src':text_node.url,
                'alt':''
            }
            return LeafNode('img', '', )

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise SyntaxError('Text missing a delimiter')
            for index, text in enumerate(split_text):
                if text != '':
                    if index%2 != 0:
                        new_nodes.append(TextNode(text, text_type))
                    else:
                        new_nodes.append(TextNode(text, TextType.PLAIN_TEXT))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    text_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return text_url

def extract_markdown_links(text: str) -> list[tuple]:
    text_url = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return text_url
    
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        text_url = extract_markdown_images(node.text)
        if node.text_type is not TextType.PLAIN_TEXT or not text_url:
            new_nodes.append(node)
        else:
            current_text = node.text
            for text, image in text_url:
                search = f'![{text}]({image})'
                sections = current_text.split(search, 1)
                if sections[0] != '':
                    new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
                current_text = sections[-1]
                new_nodes.append(TextNode(text, TextType.IMAGES, image))
            if current_text != '':
                new_nodes.append(TextNode(current_text, TextType.PLAIN_TEXT))
    return new_nodes

def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        text_url = extract_markdown_links(node.text)
        if node.text_type is not TextType.PLAIN_TEXT or not text_url:
            new_nodes.append(node)
        else:
            current_text = node.text
            for text, link in text_url:
                search = f'[{text}]({link})'
                sections = current_text.split(search, 1)
                if sections[0] != '':
                    new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
                current_text = sections[-1]
                new_nodes.append(TextNode(text, TextType.LINK_TEXT, link))
            if current_text != '':
                new_nodes.append(TextNode(current_text, TextType.PLAIN_TEXT))
    return new_nodes

def text_to_textnode(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

def extract_title(markdown: str):
    title = markdown.split('\n', 1)[0][2:].strip()
    if not title:
        raise Exception('No title')
    return title
                