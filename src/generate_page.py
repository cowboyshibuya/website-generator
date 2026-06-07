from logging import root
import os
import pathlib

from block_markdown import markdown_to_html_node
from inline_markdown import extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    if not from_path or not dest_path:
        raise Exception("incorrect paths")

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_content = ""
    if os.path.exists(from_path) and os.path.isfile(from_path):
        with open(from_path, 'r') as file:
            md_content = file.read()

    template_content = ""
    if os.path.exists(template_path) and os.path.isfile(template_path):
        with open(template_path, 'r') as file:
            template_content = file.read()

    html = markdown_to_html_node(md_content).to_html()

    title = extract_title(md_content)

    page = template_content.replace("{{ Title }}", title, 1)
    page = page.replace("{{ Content }}", html)

    if not basepath.endswith("/"):
        basepath += "/"
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)

    if dest_dir :
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath, root_path=None):
    if not dir_path_content:
        raise Exception("no dir path content")

    if root_path is None:
        root_path = dir_path_content
    # crawl every entry in the content directory
    files = os.listdir(dir_path_content)

    for file in files:
        # for each markdown file found, generate a new .html file using the same template.html
        print("files : ", files)
        filepath = os.path.join(dir_path_content, file)
        #print("file path :", filepath)

        if os.path.isdir(filepath):
            print(f"{file} is a directory")
            generate_pages_recursive(filepath, template_path, dest_dir_path, basepath, root_path)
            continue

        if os.path.isfile(filepath):
            print(f"{file} is a file.")
            if filepath.endswith(".md"):
                print(f"{file} : files ends with .md")
                # the generate pages should be written to the public directory in the same directory structure
                #print("File path using pathlib : ", pathlib.Path(filepath).relative_to(dir_path_content))
                rel_filepath = os.path.relpath(filepath, root_path)
                destination_path = os.path.join(dest_dir_path, rel_filepath)
                destination_path = destination_path.replace(".md", ".html")
                generate_page(filepath, template_path, destination_path, basepath)
                continue
                # path_parts = filepath.split(dir_path_content)
                # print("path parts : ", path_parts)
