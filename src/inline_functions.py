import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Delimiter {delimiter} does not have a correct match in given text: {old_node.text}.")
        new_node = []
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_node.append(TextNode(part, TextType.TEXT))
            else:
                new_node.append(TextNode(part, text_type))
        new_nodes.extend(new_node)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if images == []:
            new_nodes.append(old_node)
            continue
        new_node = []
        text = old_node.text
        pattern = r"(!\[.+?\]\(.+?\))"
        parts = re.split(pattern, text)
        ind = 0
        for part in parts:
            if part == "":
                continue
            if re.match(pattern, part):
                image = images[ind]
                alt = image[0]
                src = image[1]
                new_node.append(TextNode(alt, TextType.IMAGE , src))
                ind += 1
            else:
                new_node.append(TextNode(part, TextType.TEXT))
        new_nodes.extend(new_node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if links == []:
            new_nodes.append(old_node)
            continue
        new_node = []
        text = old_node.text
        pattern = r"(\[.+?\]\(.+?\))"
        parts = re.split(pattern, text)
        ind = 0 
        for part in parts:
            if part == "":
                continue
            if re.match(pattern, part):
                link = links[ind]
                descr = link[0]
                href = link[1]
                new_node.append(TextNode(descr, TextType.LINK, href))
                ind += 1
            else:
                new_node.append(TextNode(part, TextType.TEXT))
        new_nodes.extend(new_node)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.+?)\]\((.+?)\)"
    images = re.findall(pattern, text)
    return images


def extract_markdown_links(text):
    pattern = r"\[(.+?)\]\((.+?)\)"
    links = re.findall(pattern, text)
    return links


def text_to_textnodes(text):
    delimiters = {"**": TextType.BOLD,
                  "_": TextType.ITALIC,
                  "`": TextType.CODE,
                }
    initial_node = TextNode(text, TextType.TEXT)
    result = split_nodes_image([initial_node])
    result = split_nodes_link(result)
    for delimiter in delimiters:
        result = split_nodes_delimiter(result, delimiter, delimiters[delimiter])
    return result

