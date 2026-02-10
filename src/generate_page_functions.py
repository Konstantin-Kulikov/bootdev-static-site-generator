import os, shutil
from block_functions import markdown_to_html_node
from content_copy import collect_filenames


def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line.lstrip('# ')
    raise Exception("Heading is not found")


def generate_page(basepath, from_path, template_path, dest_path):
    with open(from_path, 'r') as f:
        raw_content = f.read()
    with open(template_path, 'r') as t:
        template = t.read()
    content = markdown_to_html_node(raw_content).to_html()
    title = extract_title(raw_content)
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    with open(dest_path, 'w') as f:
        f.write(template)


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    filenames = [i for i in collect_filenames(dir_path_content) if i.endswith('.md')]
    for filename in filenames:
        dirname = os.path.dirname(filename.replace(dir_path_content, "")).lstrip('/')
        dest_dir = os.path.join(dest_dir_path, dirname)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
        html_file = os.path.basename(filename).replace('.md', '.html')
        html_file = os.path.join(dest_dir, html_file)
        generate_page(basepath, filename, template_path, html_file)
    