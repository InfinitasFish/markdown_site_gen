from enum import Enum
from nodes import LeafNode, ParentNode, TextType
from inline import text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = 1,
    HEADING = 2,
    CODE = 3,
    QUOTE = 4,
    UNORDERED_LIST = 5,
    ORDERED_LIST = 6


def block_to_block_type(block_text):
    if block_text.split() and '#' in block_text.split()[0]:
        return BlockType.HEADING
    elif block_text.startswith('```\n') and block_text.endswith('```'):
        return BlockType.CODE
    elif block_text.startswith('>'):
        return BlockType.QUOTE
    elif block_text.startswith('- '):
        return BlockType.UNORDERED_LIST
    elif block_text.startswith('1. '):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block:
            filtered_blocks.append(block)
    return filtered_blocks


def markdown_paragraph_block_to_html(block):
    block_nodes = text_to_textnodes(block)
    local_children = []
    for text_node in block_nodes:
        leaf_node = text_node_to_html_node(text_node)
        local_children.append(leaf_node)

    parent_node = ParentNode('p', local_children, props=None)
    return parent_node


def markdown_header_block_to_html(block):
    hash_count = 0
    while block[hash_count] == '#' and hash_count < len(block):
        hash_count += 1
    block = block[hash_count:].strip()

    local_children = []
    block_nodes = text_to_textnodes(block)
    for text_node in block_nodes:
        leaf_node = text_node_to_html_node(text_node)
        local_children.append(leaf_node)

    parent_node = ParentNode(f'h{hash_count}', local_children, props=None)
    return parent_node


# create single LeafNode without addition inline parsing (because it's code block)
def markdown_code_block_to_html(block):
    code_text = block.split('```')[1]
    parent_node = ParentNode('pre', [LeafNode('code', code_text, props=None)], props=None)
    return parent_node


# > text -> >text, removing redundant space here
def markdown_quote_block_to_html(block):
    quote_text = block.split('>', 1)[1].strip()
    block_nodes = text_to_textnodes(quote_text)
    local_children = []
    for text_node in block_nodes:
        leaf_node = text_node_to_html_node(text_node)
        local_children.append(leaf_node)
    parent_node = ParentNode('blockquote', local_children, props=None)
    return parent_node


def markdown_unordered_list_to_html(block):
    # first item after splitting will be ''
    list_items = list(map(str.strip, block.split('-')))[1:]
    local_children = []
    for list_item in list_items:
        list_item_nodes = text_to_textnodes(list_item)
        item_children = [text_node_to_html_node(text_node) for text_node in list_item_nodes]
        item_parent_node = ParentNode('li', children=item_children, props=None)
        local_children.append(item_parent_node)
    parent_node = ParentNode('ul', local_children, props=None)
    return parent_node


def markdown_ordered_list_to_html(block):
    # splitting by new lines, then cut off numbering like: 1. 2. ... 13. 
    list_items = block.split('\n')
    local_children = []
    for list_item in list_items:
        numbering_len = 0
        while list_item[numbering_len] != '.':
            numbering_len += 1
        list_item = list_item[numbering_len+1:].strip()

        # same logic as for unordered list
        list_item_nodes = text_to_textnodes(list_item)
        item_children = [text_node_to_html_node(text_node) for text_node in list_item_nodes]
        item_parent_node = ParentNode('li', children=item_children, props=None)
        local_children.append(item_parent_node)

    parent_node = ParentNode('ol', local_children, props=None)
    return parent_node


def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    div_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            div_children.append(markdown_paragraph_block_to_html(block))
        elif block_type == BlockType.HEADING:
            div_children.append(markdown_header_block_to_html(block))
        elif block_type == BlockType.CODE:
            div_children.append(markdown_code_block_to_html(block))
        elif block_type == BlockType.QUOTE:
            div_children.append(markdown_quote_block_to_html(block))
        elif block_type == BlockType.UNORDERED_LIST:
            div_children.append(markdown_unordered_list_to_html(block))
        elif block_type == BlockType.ORDERED_LIST:
            div_children.append(markdown_ordered_list_to_html(block))
        else:
            raise ValueError(f'Invalid BlockType in markdown_to_html(): {block_type}')

    div_parent = ParentNode('div', children=div_children, props=None)
    return div_parent.to_html()
