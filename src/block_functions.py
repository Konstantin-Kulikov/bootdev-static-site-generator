import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_functions import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


def block_to_block_type(markdown):
    if re.match("^#{1,6} ", markdown):
        return BlockType.HEADING
    elif markdown.startswith('```') and markdown.endswith('```'):
        return BlockType.CODE
    elif re.match("^>.*", markdown):
        return BlockType.QUOTE
    elif re.match("^- ", markdown):
        return BlockType.UNORDERED_LIST
    elif re.match("^\d\.", markdown):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    raw_split = markdown.split("\n\n")
    clean_split = [_.strip() for _ in raw_split if _]
    return clean_split


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
            html_node = block_to_html_node(block)
            children.append(html_node)
    main = ParentNode("div", children)
    return main


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return list_to_html(block, True)
    elif block_type == BlockType.UNORDERED_LIST:
        return list_to_html(block, False)


def paragraph_to_html_node(block):
    block = block.replace('\n', ' ')
    block_text_nodes = text_to_textnodes(block)
    block_html_nodes = [text_node_to_html_node(_).to_html() for _ in block_text_nodes]
    block_html_text = "".join(block_html_nodes)
    html_node = LeafNode("p", block_html_text)
    return html_node


def code_to_html_node(block):
    clean_block =  block.replace('```\n', '').replace('```', '')
    text_node = TextNode(clean_block, TextType.CODE)
    html_node = text_node_to_html_node(text_node)
    code_parent = ParentNode("pre", [html_node])
    return code_parent


def quote_to_html_node(block):
    clean_block = block.split('\n')
    quote = []
    for line in clean_block:
        if line.startswith('>'):
            quote.append(line.replace('> ', ''))
    quote = " ".join(quote)
    quote_node = LeafNode("blockquote", quote)
    return quote_node


def heading_to_html_node(block):
    level = block.count('#')
    text = block.replace('#', '')
    node = LeafNode(f'h{level}', text.strip())
    return node


def list_to_html(block, ordered):
    block_list = block.split('\n')
    points = []
    for point in block_list:
        if not ordered:
            clean_point = point.lstrip('- ')
        else:
            clean_point = point[point.find(' ')+1:]
        point_nodes = text_to_textnodes(clean_point)
        point_html_list = [text_node_to_html_node(i).to_html() for i in point_nodes]
        point_html = "".join(point_html_list)
        node = LeafNode('li', point_html)
        points.append(node)
    if ordered:
        return ParentNode('ol', points)
    else:
        return ParentNode('ul', points)
