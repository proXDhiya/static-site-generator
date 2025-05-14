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
        return LeafNode(tag='img', value=None, props={'src': text_node.url, 'alt': text_node.text})
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
