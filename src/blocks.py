from enum import Enum
from textnode import *
from htmlnode import *

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'

def markdown_to_blocks(markdown: str):
    markdown = markdown.strip()
    blocks = markdown.split('\n\n')
    for block in blocks:
        block = block.strip('')
        if block == '':
            del block
    return blocks 

def block_to_block_type(block: str):
    headings = ('# ','## ','### ','#### ','##### ','###### ')
    lines = block.split('\n')
    if block.startswith(headings):
        return BlockType.HEADING
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f'{start}. ') for start, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnode(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes

def paragraph_to_html_node(block: str) -> ParentNode:
    block = block.replace('\n',' ')
    nodes = text_to_children(block)
    return ParentNode('p', nodes)

def heading_to_html_node(block: str) -> ParentNode:
    header = ''
    for char in block:
        if char == '#':
            header += '#'
        elif char != '#':
            break
    header_count = len(header)
    text = block[header_count+1:]
    nodes = text_to_children(text)
    return ParentNode(f'h{header_count}', nodes)

def code_to_html_node(block: str) -> ParentNode:
    text = block[4:-3]
    node = [text_node_to_html_node(TextNode(text, TextType.CODE_TEXT))]
    return ParentNode('pre',node)

def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split('\n')
    separated_lines = []
    for line in lines:
        if line.startswith('> '):
            separated_lines.append(line[2:])
        elif line.startswith('>'):
            separated_lines.append(line[1:])
    combined_lines = ' '.join(separated_lines)
    nodes = text_to_children(combined_lines)
    return ParentNode('blockquote', nodes)

def unordered_list_to_html_node(block: str) -> ParentNode:
    lines = block.split('\n')
    nodes = []
    for line in lines:
        children = text_to_children(line[2:])
        nodes.append(ParentNode('li', children))
    return ParentNode('ul', nodes)

def ordered_list_to_html_node(block:str) -> ParentNode:
    lines = block.split('\n')
    nodes = [] 
    for index, line in enumerate(lines):
        children = text_to_children(line[len(str(index+1))+2:])
        nodes.append(ParentNode('li', children))
    return ParentNode('ol', nodes)
            
    
    
def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                nodes.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                nodes.append(heading_to_html_node(block))
            case BlockType.CODE:
                nodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                nodes.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                nodes.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                nodes.append(ordered_list_to_html_node(block))
    return ParentNode('div', nodes)

