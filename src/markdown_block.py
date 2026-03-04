import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_inline import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_block):
    block_lines_list = markdown_block.split("\n")
    heading_pattern = r"^#{1,6} "
    
    if re.match(heading_pattern, markdown_block):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```") and len(block_lines_list) >= 2:
        return BlockType.CODE
    elif all(line.startswith(">") for line in block_lines_list):
        return BlockType.QUOTE
    elif all(line.startswith("- ") or line.startswith("* ") for line in block_lines_list):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(block_lines_list, start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = []
    parts = markdown.split('\n\n')
    for part in parts:
        stripped_part = part.strip()
        if stripped_part == "":
            continue
        blocks.append(stripped_part)
    return blocks


def text_to_children(text):
    """
    Takes a raw string, turns it into TextNodes, then converts those into HTMLNodes
    """
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type_of_block = block_to_block_type(block)
        if type_of_block is BlockType.PARAGRAPH:
            tag = "p"
            cleaned_text = block.replace("\n", " ")
            children = text_to_children(cleaned_text)
            parentnode = ParentNode(tag = tag, children = children, props = None)
            nodes.append(parentnode)
        elif type_of_block is BlockType.HEADING:
            tag = f"h{type_of_heading(block)}"
            children = text_to_children(heading_text(block))
            parentnode = ParentNode(tag = tag, children = children, props = None)
            nodes.append(parentnode)
        elif type_of_block is BlockType.CODE:
            child_tag = "code"
            cleaned_code = block[3:-3]
            code_text_node = TextNode(cleaned_code, TextType.TEXT)
            code_html_node = text_node_to_html_node(code_text_node)
            code_node = ParentNode(tag=child_tag, children=[code_html_node])
            parent_tag = "pre"
            parentnode = ParentNode(tag=parent_tag, children=[code_node])
            nodes.append(parentnode)
        elif type_of_block is BlockType.QUOTE:
            cleaned_quote = ""
            cleaned_lines = []
            tag = "blockquote"
            quote_lines = block.split("\n")
            for line in quote_lines:
                if line.startswith(">"):
                    line = line[1:].strip()
                cleaned_lines.append(line)
            cleaned_quote = " ".join(cleaned_lines)
            children = text_to_children(cleaned_quote)
            parentnode = ParentNode(tag = tag, children = children, props = None)
            nodes.append(parentnode)
        elif type_of_block is BlockType.UNORDERED_LIST:
            ulist_lines = block.split("\n")
            li_list = []
            child_tag = "li"
            for line in ulist_lines:
                if line.startswith("- ") or line.startswith("* "):
                    line = line[1:].strip()
                children = text_to_children(line)
                li_node = ParentNode(tag = child_tag, children = children, props = None)
                li_list.append(li_node)
            parent_tag = "ul"
            parentnode = ParentNode(tag = parent_tag, children = li_list, props = None)
            nodes.append(parentnode)
        elif type_of_block is BlockType.ORDERED_LIST:
            olist_lines = block.split("\n")
            li_list = []
            child_tag = "li"
            for line in olist_lines:
                # line format is expected to be: "1. item", "2. item", ...
                # remove the leading "<number>. "
                _, item_text = line.split(". ", 1)
                children = text_to_children(item_text)
                li_node = ParentNode(tag=child_tag, children=children, props=None)
                li_list.append(li_node)
            parent_tag = "ol"
            parentnode = ParentNode(tag=parent_tag, children=li_list, props=None)
            nodes.append(parentnode)
    return ParentNode(tag = "div", children = nodes, props = None)


def type_of_heading(markdown: str) -> int | None:
    match = re.match(r'^(#{1,6})\s', markdown)
    if not match:
        return None  # Not a heading
    return len(match.group(1))


def heading_text(markdown: str) -> str | None:
    if type_of_heading(markdown) is None:
        return None # Not a heading
    return markdown[type_of_heading(markdown)+1:]