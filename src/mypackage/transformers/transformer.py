from mypackage.nodes.textnode import TextNode, TextType
from mypackage.nodes.htmlnode import LeafNode


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
    url_name, rest = part.split(']', 1)
    url_path = rest.split('(', 1)[1].split(')', 1)[0]
    rest_text = rest.split(')', 1)[1].strip()
    return url_name, url_path, rest_text


def parse_image(part):
    alt_text = part.split('[', 1)[1].split(']', 1)[0]
    src_url = part.split('](', 1)[1].split(')', 1)[0]
    rest_text = part.split(')', 1)[1].strip()
    return alt_text, src_url, rest_text


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        parts = node.text.split(delimiter)

        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, node.text_type))
            else:
                if text_type == TextType.LINK:
                    url_name, url_path, rest_text = parse_link(part)
                    new_nodes.append(TextNode(url_name, TextType.LINK, url_path))
                    if rest_text:
                        new_nodes.append(TextNode(rest_text, node.text_type))

                elif text_type == TextType.IMAGE:
                    alt_text, src_url, rest_text = parse_image(part)
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, src_url))
                    if rest_text:
                        new_nodes.append(TextNode(rest_text, node.text_type))

                else:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes
