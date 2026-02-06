from __future__ import annotations
from enum import Enum


class TextType(Enum):
    TEXT = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other: TextNode):
        return (self.text == other.text and self.text_type == other.text_type 
                and self.url == other.url)
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self):
        res = ''
        if self.props:
            for k, v in self.props.items():
                res += f' {k}="{v}"'
        return res

    def to_html(self):
        raise NotImplementedError('hehe')
        html_props = self.props_to_html()
        return f'<{self.tag} {html_props}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError('empty value in LeafNode.to_html()')

        if not self.tag:
            return f'{self.value}'
        else:
            html_props = self.props_to_html()
            return f'<{self.tag}{html_props}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, None, {self.props})' 
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError('empty tag in ParentNode')
        if not self.children:
            raise ValueError('empty children in ParentNode')

        children_html = ''.join([child.to_html() for child in self.children])
        return f'<{self.tag}>{children_html}</{self.tag}>'
    
