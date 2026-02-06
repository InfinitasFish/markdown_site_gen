import unittest
from nodes import (TextNode, TextType, HTMLNode, 
    LeafNode, ParentNode)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_node(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a image node", TextType.IMAGE, url='/test/url')
        self.assertNotEqual(node, node2) 

    def test_not_eq_url(self):
        node = TextNode("This is a image node", TextType.IMAGE)
        node2 = TextNode("This is a image node", TextType.IMAGE, url='/test/url')
        self.assertNotEqual(node, node2)


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_first(self):
        node = HTMLNode(props={"href": "https://www.google.com", 
                               "target": "_blank",})
        expected_props_html = ' href="https://www.google.com" target="_blank"'
        node_props_html = node.props_to_html()
        self.assertEqual(expected_props_html, node_props_html)

    def test_props_to_html_second(self):
        node = HTMLNode(props={"text": "alternative text", 
                               "style": "color: blue; font-size: 50px",})
        expected_props_html = ' text="alternative text" style="color: blue; font-size: 50px"'
        node_props_html = node.props_to_html()
        self.assertEqual(expected_props_html, node_props_html)

    def test_props_to_html_type(self):
        node = HTMLNode(props={"text": "how are you?"})
        node_props_html = node.props_to_html()
        self.assertEqual(type(node_props_html), str)



class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_no_children(self):
        node = LeafNode("p", "Hello, world!")
        node_wchildren = LeafNode('p', 'hi', props=None)
        self.assertEqual(None, node_wchildren.children)

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "dum dum dum", props={'href': 'https://lmao.com', 'alt': 'empty link'})
        expected_html_str = '<a href="https://lmao.com" alt="empty link">dum dum dum</a>'
        real_html_str = node.to_html()
        self.assertEqual(expected_html_str, real_html_str)


class TestParentNode(unittest.TestCase):
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
    
    def test_to_html_very_nested(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        another_child = LeafNode("a", "dum dum dum", props={'href': 'https://lmao.com', 'alt': 'empty link'})
        parent_with_child = ParentNode('i', [another_child])
        parent_node = ParentNode("div", [child_node, parent_with_child])
        expected_html = '<div><span><b>grandchild</b></span><i><a href="https://lmao.com" alt="empty link">dum dum dum</a></i></div>'
        real_html = parent_node.to_html()
        self.assertEqual(expected_html, real_html)


if __name__ == '__main__':
    unittest.main()


