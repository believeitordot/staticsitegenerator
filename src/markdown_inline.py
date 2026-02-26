import re
from typing import List, Tuple
from textnode import TextType, TextNode


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    for alt, url in re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text):
        # Unwrap <...> URLs if present
        if url.startswith("<") and url.endswith(">"):
            url = url[1:-1]
        # Unescape common escapes in alt text
        alt = alt.replace(r"\[", "[").replace(r"\]", "]").replace(r"\\", "\\")
        results.append((alt, url))
    return results


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    for anchor, url in re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text):
        # Unwrap <...> URLs if present
        if url.startswith("<") and url.endswith(">"):
            url = url[1:-1]
        # Unescape common escapes in anchor text
        anchor = (
            anchor
            .replace(r"\[", "[")
            .replace(r"\]", "]")
            .replace(r"\\", "\\")
        )
        results.append((anchor, url))
    return results


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        splitted_node = old_node.text.split(delimiter)
        if len(splitted_node) % 2 == 0:
            raise ValueError("No matching closing delimiter found")
        else:
            for i in range(len(splitted_node)):
                if splitted_node[i] == "":
                    continue
                if i % 2 != 0:
                    new_nodes.append(TextNode(splitted_node[i], text_type))
                else:
                    new_nodes.append(TextNode(splitted_node[i], TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Pass through anything that's not plain text
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        # If there are no images, keep the node as-is
        if not images:
            new_nodes.append(old_node)
            continue
        remaining = old_node.text
        for image_alt, image_link in images:
            marker = f"![{image_alt}]({image_link})"
            sections = remaining.split(marker, 1)
            # If the marker isn't found, stop trying to split (avoid IndexError/dup bugs)
            if len(sections) == 1:
                break
            before, after = sections
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            # Keep consuming from the right side
            remaining = after
        # Whatever's left after the last image stays as text
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Pass through anything that's not plain text
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        # No links → keep node unchanged
        if not links:
            new_nodes.append(old_node)
            continue
        remaining = old_node.text
        for anchor_text, url in links:
            marker = f"[{anchor_text}]({url})"
            sections = remaining.split(marker, 1)
            # Defensive guard in case of mismatch
            if len(sections) == 1:
                break
            before, after = sections
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            remaining = after
        # Append leftover text
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    # Start with a single TEXT node containing the whole string
    nodes = [TextNode(text, TextType.TEXT)]

    # Split by inline formatting delimiters first
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Then split out images and links from the remaining TEXT nodes
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes