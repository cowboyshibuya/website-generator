import os

from block_markdown import markdown_to_html_node
from inline_markdown import extract_title

def generate_page(from_path, template_path, dest_path):
    if not from_path or not dest_path:
        raise Exception("incorrect paths")

    # should print a message like "Generating page from ... to ... using ... template"
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # read md file at from_path and store the contents in a variable
    md_content = ""
    if os.path.exists(from_path) and os.path.isfile(from_path):
        with open(from_path, 'r') as file:
            md_content = file.read()
            #print("content : ", md_content)

    # Read the template file at template_path and store the contents in a variable.
    template_content = ""
    if os.path.exists(template_path) and os.path.isfile(template_path):
        with open(template_path, 'r') as file:
            template_content = file.read()
            #print("template content :", template_content)


    # Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
    html = markdown_to_html_node(md_content).to_html()

    # Use the extract_title function to grab the title of the page.
    title = extract_title(md_content)

    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    replaced_template_title = template_content.replace("{{ Title }}", title, 1)
    replaced_template_content = replaced_template_title.replace("{{ Content }}", html)

    # Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    if not os.path.dirname(dest_path):
        print("No existing directory")

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(replaced_template_content)
