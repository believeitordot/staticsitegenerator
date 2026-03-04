import os
from pathlib import Path
from markdown_block import markdown_to_html_node
from htmlnode import ParentNode


def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path}, saving it in {dest_path} using {template_path}")

    # Read markdown file
    with open(from_path, "r") as f:
        markdown_string = f.read()

    # Read html template
    with open(template_path, "r") as f:
        template_string = f.read()

    html_string = markdown_to_html_node(markdown_string).to_html()

    page_title = extract_title(markdown_string)

    template_string = template_string.replace('{{ Title }}', page_title)

    template_string = template_string.replace('{{ Content }}', html_string)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        written = f.write(template_string)



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    with os.scandir(dir_path_content) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".md"):
                new_path = Path(entry.name).with_suffix(".html")
                generate_page(entry.path, template_path, os.path.join(dest_dir_path, new_path))
            elif entry.is_dir():
                new_path = Path(entry.name)
                generate_pages_recursive(entry.path, template_path, os.path.join(dest_dir_path, new_path))
