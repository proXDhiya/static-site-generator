import unittest
from mypackage.nodes.blocknode import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_blocks(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("####### Invalid"), BlockType.HEADING)

    def test_code_blocks(self):
        code_block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

        not_code = "`` print('Hello') ``"
        self.assertNotEqual(block_to_block_type(not_code), BlockType.CODE)

    def test_quote_blocks(self):
        quote_block = "> line 1\n> line 2\n> line 3"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

        mixed_quote = "> line 1\nnot quoted"
        self.assertNotEqual(block_to_block_type(mixed_quote), BlockType.QUOTE)

    def test_unordered_list_blocks(self):
        ul_block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(ul_block), BlockType.UNORDERED_LIST)

        invalid_ul_block = "- item 1\n* item 2"
        self.assertNotEqual(block_to_block_type(invalid_ul_block), BlockType.UNORDERED_LIST)

    def test_ordered_list_blocks(self):
        ol_block = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ORDERED_LIST)

        wrong_numbers = "1. item 1\n3. item 2"
        self.assertNotEqual(block_to_block_type(wrong_numbers), BlockType.ORDERED_LIST)

        mixed_ol = "1. item 1\n2. item 2\n- not valid"
        self.assertNotEqual(block_to_block_type(mixed_ol), BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        para1 = "This is a single paragraph."
        self.assertEqual(block_to_block_type(para1), BlockType.PARAGRAPH)

        para2 = "This is a paragraph\nthat spans multiple lines\nwithout special markdown."
        self.assertEqual(block_to_block_type(para2), BlockType.PARAGRAPH)


if __name__ == '__main__':
    unittest.main()
