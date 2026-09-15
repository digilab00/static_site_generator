from enum import Enum

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
        if (self.text, self.text_type, self.url) == (node.text, node.text_type, node.url):
            return True
        return False

    def __repr__(self):
        print(f'TextNode(f{self.text}, f{self.text_type}, f{self.url}')
        
    
    