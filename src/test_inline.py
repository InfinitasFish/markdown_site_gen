import unittest
from nodes import TextType, TextNode, LeafNode
from inline import (text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
    split_nodes_image, split_nodes_link, text_to_textnodes)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_image(self):
        node = TextNode('hello world image', TextType.IMAGE, 'https://nonexistent_link.com')
        leaf_node = text_node_to_html_node(node)
        leaf_node_html = leaf_node.to_html()
        self.assertEqual(leaf_node_html, f'<img src="{node.url}" alt="{node.text}">{node.text}</img>')


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_center_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        real_new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [TextNode("This is text with a ", TextType.TEXT), 
                          TextNode("code block", TextType.CODE), 
                          TextNode(" word", TextType.TEXT),]

        self.assertEqual(expected_nodes, real_new_nodes)

    def test_alot_delimiters(self):
        node = TextNode('text **with** a **lot** of **delimiters**', TextType.TEXT)
        real_splitted_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [TextNode("text ", TextType.TEXT), TextNode("with", TextType.BOLD), 
                          TextNode(" a ", TextType.TEXT), TextNode("lot", TextType.BOLD),
                          TextNode(" of ", TextType.TEXT), TextNode("delimiters", TextType.BOLD),]
        self.assertEqual(expected_nodes, real_splitted_nodes)

    def test_continius_delims(self):
        node = TextNode('text with _different_ **delimiters**', TextType.TEXT)
        nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        real_splitted_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        expected_nodes = [TextNode('text with ', TextType.TEXT), TextNode('different', TextType.ITALIC),
                          TextNode(' ', TextType.TEXT), TextNode('delimiters', TextType.BOLD),]
        self.assertEqual(expected_nodes, real_splitted_nodes)


class TextRegexExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/@something)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/@something")], matches)

    def test_extract_markdown_links_and_images(self):
        text = "This is text with an [link](https://i.imgur.com/@something) This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        matches.extend(extract_markdown_links(text))
        links = [("link", "https://i.imgur.com/@something")]
        images = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(images + links, matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_two_image_another(self):
        node = TextNode(
            "This is text with a image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        real_new_nodes = split_nodes_image([node])
        expected_new_nodes = [TextNode('This is text with a image ', TextType.TEXT), TextNode('to boot dev', TextType.IMAGE, 'https://www.boot.dev'),
            TextNode(' and ', TextType.TEXT), TextNode('to youtube', TextType.IMAGE, 'https://www.youtube.com/@bootdotdev'),]
        self.assertEqual(expected_new_nodes, real_new_nodes)

    def test_zero_images(self):
        node = TextNode(
            "This is text with a image and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        real_new_nodes = split_nodes_image([node])
        expected_new_nodes = [TextNode('This is text with a image and [to youtube](https://www.youtube.com/@bootdotdev)', TextType.TEXT)]
        self.assertEqual(expected_new_nodes, real_new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_two_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        real_new_nodes = split_nodes_link([node])
        expected_new_nodes = [TextNode('This is text with a link ', TextType.TEXT), TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
            TextNode(' and ', TextType.TEXT), TextNode('to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev'),]
        self.assertEqual(expected_new_nodes, real_new_nodes)
    
    def test_two_link_another(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)w[hi](https://are/you/watching) and image ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        real_new_nodes = split_nodes_link([node])
        expected_new_nodes = [TextNode('This is text with a link ', TextType.TEXT), TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
            TextNode('w', TextType.TEXT), TextNode('hi', TextType.LINK, 'https://are/you/watching'), 
            TextNode(' and image ![to youtube](https://www.youtube.com/@bootdotdev)', TextType.TEXT)]
        self.assertEqual(expected_new_nodes, real_new_nodes)

    def test_zero_link(self):
        node = TextNode(
            "This is text with a image and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        real_new_nodes = split_nodes_link([node])
        expected_new_nodes = [TextNode('This is text with a image and ![to youtube](https://www.youtube.com/@bootdotdev)', TextType.TEXT)]
        self.assertEqual(expected_new_nodes, real_new_nodes)
    
    def test_link_and_image(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)w[hi](https://are/you/watching) and image ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        real_new_nodes = split_nodes_link([node])
        real_new_nodes = split_nodes_image(real_new_nodes)
        expected_new_nodes = [TextNode('This is text with a link ', TextType.TEXT), TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
            TextNode('w', TextType.TEXT), TextNode('hi', TextType.LINK, 'https://are/you/watching'), 
            TextNode(' and image ', TextType.TEXT), TextNode('to youtube', TextType.IMAGE, 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(expected_new_nodes, real_new_nodes)


class TestTextToNodesWrapper(unittest.TestCase):
    def test_consecutive_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        real_nodes = text_to_textnodes(text)
        expected_nodes = [TextNode("This is ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC), TextNode(" word and a ", TextType.TEXT), TextNode("code block", TextType.CODE), 
            TextNode(" and an ", TextType.TEXT), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev"),]
        self.assertEqual(expected_nodes, real_nodes)

    def test_consecutive_types_another(self):
        text = "This is **text** **bold** **more bold hiiii [][][][]** and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) _just for fun i guess_"
        real_nodes = text_to_textnodes(text)
        expected_nodes = [TextNode("This is ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(' ', TextType.TEXT), 
            TextNode("bold", TextType.BOLD), TextNode(' ', TextType.TEXT), TextNode("more bold hiiii [][][][]", TextType.BOLD),
            TextNode(' and an ', TextType.TEXT), TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode(' ', TextType.TEXT), TextNode('just for fun i guess', TextType.ITALIC),]
        self.assertEqual(expected_nodes, real_nodes)
