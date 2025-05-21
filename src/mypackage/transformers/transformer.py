from mypackage.nodes.textnode import TextNode, TextType
from mypackage.nodes.htmlnode import LeafNode
import re


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag='b', value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag='i', value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag='code', value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag='img', value="", props={'src': text_node.url, 'alt': text_node.text})
    raise Exception("Not implemented type")


def parse_link(part):
    match = re.match(r'\[(.*?)\]\((.*?)\)', part)
    if not match:
        raise ValueError(f"Invalid link format: {part}")
    url_name, url_path = match.groups()
    rest_text = part[match.end():].strip()
    return url_name, url_path, rest_text


def parse_image(part):
    match = re.match(r'!\[(.*?)\]\((.*?)\)', part)
    if not match:
        raise ValueError(f"Invalid image format: {part}")
    alt_text, src_url = match.groups()
    rest_text = part[match.end():].strip()
    return alt_text, src_url, rest_text


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if text_type == TextType.LINK:
            pattern = r'\[.*?\]\(.*?\)'
        elif text_type == TextType.IMAGE:
            pattern = r'!\[.*?\]\(.*?\)'
        else:
            pattern = re.escape(delimiter) + r'(.*?)' + re.escape(delimiter)

        last_end = 0
        for match in re.finditer(pattern, node.text):
            start, end = match.span()
            if start > last_end:
                new_nodes.append(TextNode(node.text[last_end:start], TextType.TEXT))

            part = match.group()
            if text_type == TextType.LINK:
                url_name, url_path, rest_text = parse_link(part)
                new_nodes.append(TextNode(url_name, TextType.LINK, url_path))
                if rest_text:
                    new_nodes.append(TextNode(rest_text, TextType.TEXT))
            elif text_type == TextType.IMAGE:
                alt_text, src_url, rest_text = parse_image(part)
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, src_url))
                if rest_text:
                    new_nodes.append(TextNode(rest_text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(match.group(1), text_type))

            last_end = end

        if last_end < len(node.text):
            new_nodes.append(TextNode(node.text[last_end:], TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    return split_nodes_delimiter(old_nodes, "", TextType.LINK)


def split_nodes_image(old_nodes):
    return split_nodes_delimiter(old_nodes, "", TextType.IMAGE)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_html_node(markdown):
    from mypackage.nodes.htmlnode import ParentNode
    from mypackage.nodes.blocknode import block_to_block_type, BlockType

    blocks = markdown_to_blocks(markdown)

    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = block.replace('\n', ' ').strip()
            text_nodes = text_to_textnodes(text)
            html_children = [text_node_to_html_node(node) for node in text_nodes]
            html_nodes.append(ParentNode(tag='p', children=html_children))

        elif block_type == BlockType.HEADING:
            headings = block.split('\n')
            for heading in headings:
                if not heading.strip():
                    continue

                level = len(heading) - len(heading.lstrip('#'))
                tag = f'h{level}'

                text = heading.strip('# ').strip()
                text_nodes = text_to_textnodes(text)
                html_children = [text_node_to_html_node(node) for node in text_nodes]
                html_nodes.append(ParentNode(tag=tag, children=html_children))

        elif block_type == BlockType.CODE:
            code_text = block.strip()[3:-3]
            code_text = code_text.lstrip('\n')
            html_nodes.append(ParentNode(tag='pre', children=[
                ParentNode(tag='code', children=[LeafNode(tag=None, value=code_text)])]))

        elif block_type == BlockType.QUOTE:
            text = block.replace('>', '', 1).replace('\n', ' ').strip()
            text_nodes = text_to_textnodes(text)
            html_children = [text_node_to_html_node(node) for node in text_nodes]
            html_nodes.append(ParentNode(tag='blockquote', children=html_children))

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split('\n')
            stack = []
            root_ul = ParentNode(tag='ul', children=[])
            stack.append((0, root_ul))
            for idx, item in enumerate(items):
                if not item.strip():
                    continue

                indent_level = len(item) - len(item.lstrip(' '))
                text = item.lstrip(' -')
                text_nodes = text_to_textnodes(text.strip())
                html_children = [text_node_to_html_node(node) for node in text_nodes]
                list_item = ParentNode(tag='li', children=html_children)
                while stack and indent_level < stack[-1][0]:
                    stack.pop()
                if indent_level > stack[-1][0]:
                    if not stack[-1][1].children:
                        pass
                    else:
                        parent_li = stack[-1][1].children[-1]
                        nested_ul = ParentNode(tag='ul', children=[])
                        parent_li.children.append(nested_ul)
                        stack.append((indent_level, nested_ul))
                stack[-1][1].children.append(list_item)
            html_nodes.append(root_ul)

        elif block_type == BlockType.ORDERED_LIST:
            items = block.split('\n')
            list_items = []
            for item in items:
                item = item.strip()
                if not item:
                    continue

                if re.match(r'^\d+\. ', item):
                    text = item[item.index('. ') + 2:]
                    text_nodes = text_to_textnodes(text)
                    html_children = [text_node_to_html_node(node) for node in text_nodes]
                    list_items.append(ParentNode(tag='li', children=html_children))

            if list_items:
                html_nodes.append(ParentNode(tag='ol', children=list_items))

    return ParentNode(tag='div', children=html_nodes)


def markdown_to_blocks(markdown):
    blocks = []
    raw_blocks = re.split(r'\n\s*\n', markdown)
    for block in raw_blocks:
        lines = block.strip('\n').split('\n')
        if not lines:
            continue

        first_line = lines[0].lstrip()
        is_list = first_line.startswith('- ') or bool(re.match(r'^\d+\. ', first_line))
        is_code = first_line.startswith('```')

        if is_code:
            cleaned_lines = [line.rstrip() for line in lines]
        elif is_list:
            leading_spaces = [
                len(line) - len(line.lstrip(' '))
                for line in lines if line.strip()
            ]
            min_leading = min(leading_spaces) if leading_spaces else 0
            cleaned_lines = [line[min_leading:].rstrip() for line in lines]
        else:
            cleaned_lines = [line.strip() for line in lines]

        block_str = '\n'.join(cleaned_lines).rstrip('\n')
        blocks.append(block_str)
    return blocks


def extract_title(markdown):
    html = markdown_to_html_node(markdown)
    for child in html.children:
        if child.tag == 'h1':
            return ''.join([c.value for c in child.children if hasattr(c, 'value') and c.value])
    raise ValueError("No title found in markdown")


def generate_page(from_path, template_path, dest_path):
    markdown_content = None
    template_content = None

    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    page_title = extract_title(markdown_content)

    html_nodes = markdown_to_html_node(markdown_content)
    html_content = html_nodes.to_html()

    final_output = template_content.replace("{{ Title }}", page_title)
    final_output = final_output.replace("{{ Content }}", html_content)

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_output)
