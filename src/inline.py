from __future__ import annotations
import re
from nodes import TextType, TextNode, LeafNode


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text, props=None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode('img', text_node.text, {'src': text_node.url, 'alt': text_node.text})


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
    splitted_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            splitted_nodes.append(node)
            continue

        node_splitted_texts = node.text.split(delimiter)
        if len(node_splitted_texts) % 2 == 0:
            raise ValueError(f'Wrong amount of delimiters: {delimiter} in {node.text}')
        
        for i, node_text in enumerate(node_splitted_texts):
            if node_text == '':
                continue
            if i % 2 == 1:
                new_node = TextNode(node_text, text_type, node.url)
            else:
                new_node = TextNode(node_text, TextType.TEXT, node.url)
            splitted_nodes.append(new_node)

    return splitted_nodes


def extract_markdown_images(text):
    markdown_image_pattern = r'\!{1}\[[a-zA-Z0-9."\'\-\_ ]+\]\((?:https?:\/\/|\/)[a-zA-Z0-9./@\'"\-\_]+\)'
    images = re.findall(markdown_image_pattern, text)
    text_url_tuples = []
    for img in images:
        txt, url = img.split(']')
        txt = txt[2:]
        url = url[1:-1]
        text_url_tuples.append((txt, url))

    return text_url_tuples


# without negative lookbehind seems impossible
def extract_markdown_links(text):
    markdown_link_pattern = r'(?<!!)\[[a-zA-Z0-9."\'\-\_ ]+\]\((?:https?:\/\/|\/)[a-zA-Z0-9./@\'"\-\_]+\)'
    links = re.findall(markdown_link_pattern, text)
    text_link_tuples = []
    for link_ in links:
        txt, link = link_.split(']')
        txt = txt[1:]
        link = link[1:-1]
        text_link_tuples.append((txt, link))
    
    return text_link_tuples


# helpers for split_nodes_image() and split_nodes_link()
def flatten_list(lst):
    flatten = []
    for e in lst:
        if type(e) == list:
            for item in e:
                flatten.append(item)
        else:
            flatten.append(e)
    return flatten


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matched_images = extract_markdown_images(node.text)
        if not matched_images:
            new_nodes.append(node)
            continue
        splitted_text = []
        delimiters = []
        for img in matched_images:
            delimiter = f'![{img[0]}]({img[1]})'
            delimiters.append(delimiter)
            if not splitted_text:
                splt_texts = node.text.split(delimiter, 1)
                splt_texts.insert(1, delimiter)
                splitted_text.extend(splt_texts)
            else:
                for i, text in enumerate(splitted_text):
                    if not delimiter in text:
                        continue
                    splt_texts = text.split(delimiter, 1)
                    splt_texts.insert(1, delimiter)
                    splitted_text[i] = splt_texts
                    splitted_text = flatten_list(splitted_text)
        
        curr_img_idx = 0
        for text in splitted_text:
            if not text: 
                continue
            if text in delimiters:
                img_text = matched_images[curr_img_idx][0]
                img_url = matched_images[curr_img_idx][1]
                new_nodes.append(TextNode(img_text, TextType.IMAGE, img_url))
                curr_img_idx += 1
            else:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matched_links = extract_markdown_links(node.text)
        if not matched_links:
            new_nodes.append(node)
            continue
        splitted_text = []
        delimiters = []
        for link in matched_links:
            delimiter = f'[{link[0]}]({link[1]})'
            delimiters.append(delimiter)
            if not splitted_text:
                splt_texts = node.text.split(delimiter, 1)
                splt_texts.insert(1, delimiter)
                splitted_text.extend(splt_texts)
            else:
                for i, text in enumerate(splitted_text):
                    if not delimiter in text:
                        continue
                    splt_texts = text.split(delimiter, 1)
                    splt_texts.insert(1, delimiter)
                    splitted_text[i] = splt_texts
                    splitted_text = flatten_list(splitted_text)
        
        curr_link_idx = 0
        for text in splitted_text:
            if not text: 
                continue
            if text in delimiters:
                link_text = matched_links[curr_link_idx][0]
                link_url = matched_links[curr_link_idx][1]
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                curr_link_idx += 1
            else:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    start_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([start_node], '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes

