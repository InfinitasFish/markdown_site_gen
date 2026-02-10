import os
from block import markdown_to_blocks, markdown_to_html


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    title = ''
    for block in blocks:
        if block.startswith('#') and len(block) > 1 and block[1] != '#':
            title = block[1:].strip()
            break

    if not title:
        raise ValueError(f'No h1 title provided in: {markdown}')
    
    return title


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as f:
        markdown_text = f.read()

    content_title = extract_title(markdown_text)
    content_parent_node_html = markdown_to_html(markdown_text)

    with open(template_path, 'r') as f:
        html_template = f.read()

    html_template = html_template.replace('{{ Title }}', content_title)
    html_template = html_template.replace('{{ Content }}', content_parent_node_html)

    dest_parent_dir = os.path.abspath(os.path.join(dest_path, os.pardir))
    if not os.path.exists(dest_parent_dir):
        os.mkdir(dest_parent_dir)
    with open(dest_path, 'w') as f:
        f.write(html_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError(f'Content dir doesnt exists in generate_pages_recursive(): {dir_path_content}')

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    for file in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(file_path):
            dest_path = dest_path.replace('.md', '.html')
            generate_page(file_path, template_path, dest_path)
        elif os.path.isdir(file_path):
            generate_pages_recursive(file_path, template_path, dest_path)
        