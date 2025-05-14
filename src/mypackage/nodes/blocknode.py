from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(markdown_block):
    lines = markdown_block.strip().splitlines()

    if re.match(r'^(#{1,6})\s+.+', lines[0]):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    elif all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.strip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.strip().startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
