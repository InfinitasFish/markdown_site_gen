import os
from nodes import TextNode, TextType
from copy_dir import copy_source_dir_to_destination
from gen import generate_pages_recursive
from root import ROOT_DIR


def main():
    source = os.path.join(ROOT_DIR, 'static')
    destination = os.path.join(ROOT_DIR, 'public')
    # clears destination before copying
    copy_source_dir_to_destination(source, destination)

    from_path = os.path.join(ROOT_DIR, 'content')
    html_template_path = os.path.join(ROOT_DIR, 'template.html')
    dest_path = os.path.join(ROOT_DIR, 'public')
    # generates pages to dist, creates dist dir if it doesnt exist
    generate_pages_recursive(from_path, html_template_path, dest_path)


if __name__ == '__main__':
    main()
