import unittest
from block import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html


class TestTextToHtml(unittest.TestCase):
    def test_paragraph_to_html(self):
        text = 'bro i\'m kinda going insane writing tests. Imagine writing code that you hope works, and then you\'re trying to break it by your **own hands** with _unit tests_...'
        real_text_html = markdown_to_html(text)
        expected_text_html = "<div><p>bro i\'m kinda going insane writing tests. Imagine writing code that you hope works, and then you\'re trying to break it by your <b>own hands</b> with <i>unit tests</i>...</p></div>"
        self.assertEqual(expected_text_html, real_text_html)

    def test_paragraph_and_code_blocks(self):
        text = 'advanced, we have two blocks now... lets even put some _italic here_\n\n ```\nlist_funny=[[[[[[[]]]]]]]\nprint(nlist_funny)```\n\n Also I found out that we can have `inline code` without pre tag'
        real_text_html = markdown_to_html(text)
        expected_text_html = '<div><p>advanced, we have two blocks now... lets even put some <i>italic here</i></p><pre><code>\nlist_funny=[[[[[[[]]]]]]]\nprint(nlist_funny)</code></pre><p>Also I found out that we can have <code>inline code</code> without pre tag</p></div>'
        self.assertEqual(expected_text_html, real_text_html)

    def test_quote_blocks(self):
        text = '###great philosophy\n\nsomeone once said\n\n > the only thing _I know_ that I know **nothing**\n\nthat was me btw before I got to know everything'
        real_text_html = markdown_to_html(text)
        expected_text_html = '<div><h3>great philosophy</h3><p>someone once said</p><blockquote>the only thing <i>I know</i> that I know <b>nothing</b></blockquote><p>that was me btw before I got to know everything</p></div>'
        self.assertEqual(expected_text_html, real_text_html)
    
    def test_images_and_links(self):
        text = 'boss i\'m tired ![image](https://image/nice/meme.png) [link](https://youtube.com/@InfinitasFish) `from collections import defaultdict\nd = defaultdict(list)`'
        real_text_html = markdown_to_html(text)
        expected_text_html = '<div><p>boss i\'m tired <img src="https://image/nice/meme.png" alt="image">image</img> <a href="https://youtube.com/@InfinitasFish">link</a> <code>from collections import defaultdict\nd = defaultdict(list)</code></p></div>'
        self.assertEqual(expected_text_html, real_text_html)

    def test_unordered_list(self):
        text = '- So\n- That\'s\n- Almost\n- It\n- **baldie**'
        real_text_html = markdown_to_html(text)
        expected_text_html = '<div><ul><li>So</li><li>That\'s</li><li>Almost</li><li>It</li><li><b>baldie</b></li></ul></div>'
        self.assertEqual(expected_text_html, real_text_html)
    
    def test_ordered_list(self):
        text = '1. So\n2. That\'s\n3. Almost\n4. It\n5. **baldie**'
        real_text_html = markdown_to_html(text)
        expected_text_html = '<div><ol><li>So</li><li>That\'s</li><li>Almost</li><li>It</li><li><b>baldie</b></li></ol></div>'
        self.assertEqual(expected_text_html, real_text_html)

    def test_headers_to_html(self):
        text = '#### HeaderLevel four'
        real_text_html = markdown_to_html(text)
        expected_text_html = '<div><h4>HeaderLevel four</h4></div>'
        self.assertEqual(expected_text_html, real_text_html)

        text = '######header level six ok'
        real_text_html = markdown_to_html(text)
        expected_text_html = '<div><h6>header level six ok</h6></div>'
        self.assertEqual(expected_text_html, real_text_html)
    
    def test_header_with_inline(self):
        text = '#### HeaderLevel four with **bold** text and some ![image](https://hello/world/@hi.png)'
        real_text_html = markdown_to_html(text)
        expected_text_html = '<div><h4>HeaderLevel four with <b>bold</b> text and some <img src="https://hello/world/@hi.png" alt="image">image</img></h4></div>'
        self.assertEqual(expected_text_html, real_text_html)


class TestBlockSplitTypes(unittest.TestCase):
    def test_blocks_basic(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""

        real_blocks = markdown_to_blocks(text)
        expected_blocks = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.',
            '- This is the first list item in a list block\n- This is a list item\n- This is another list item',]
        self.assertEqual(expected_blocks, real_blocks)

    def test_blocks_basic_another(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and 

```
code here```


This is the same paragraph on a new line

- This is a list
- with items
        """
        real_blocks = markdown_to_blocks(md)
        expected_blocks = ["This is **bolded** paragraph", "This is another paragraph with _italic_ text and", "```\ncode here```", "This is the same paragraph on a new line",
                "- This is a list\n- with items",]
        self.assertEqual(expected_blocks, real_blocks)

    def test_block_type_conversion(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        
        blocks = markdown_to_blocks(text)
        real_blocks_types = []
        for block in blocks:
            real_blocks_types.append(block_to_block_type(block))
        expected_blocks_types = [BlockType.HEADING, BlockType.PARAGRAPH, BlockType.UNORDERED_LIST]
        self.assertEqual(expected_blocks_types, real_blocks_types)

    def test_block_type_conversion_another(self):
        text = """# This is a heading

#### This is a heading of text. It has some **bold** and _italic_ words inside of it.

dont forget paragraph

> hello world said the world itself

```
code block nice bro I'm somewhat of a coder myself```

1. This is the first list item in a list block
2. This is a list item
3. This is another list item"""

        blocks = markdown_to_blocks(text)
        real_blocks_types = []
        for block in blocks:
            real_blocks_types.append(block_to_block_type(block))
        expected_blocks_types = [BlockType.HEADING, BlockType.HEADING, BlockType.PARAGRAPH, 
            BlockType.QUOTE, BlockType.CODE, BlockType.ORDERED_LIST]
        self.assertEqual(expected_blocks_types, real_blocks_types)

