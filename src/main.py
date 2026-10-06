import sys

from textnode import *
from htmlnode import *
from blocks import *
import os
import shutil

def clean_dir(dir: str) -> None:
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)

def copy_static(source: str, dest: str) -> None:
    for file in os.listdir(source):
        source_path = os.path.join(source, file)
        dest_path = os.path.join(dest, file)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            copy_static(source_path, dest_path)
        print(f'Copied {source_path} into {dest_path}')

def generate_page(src_path, template_path, dest_path, basepath):
    print(f'Generating page from {src_path} to {dest_path} with template {template_path}')
    dir_path = os.path.dirname(dest_path)
    if dir_path != '' and not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(src_path, 'r') as f:
        src_file = f.read()
    with open(template_path, 'r') as f:
        template_file = f.read()  
        
    html_from = markdown_to_html_node(src_file).to_html()
    title = extract_title(src_file)

    template_file = template_file.replace('{{ Title }}', title).replace('{{ Content }}', html_from)
    template_file = template_file.replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')
    with open(dest_path, 'w') as f:
        f.write(template_file)
    return src_path, template_path, dest_path

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_path):
            dest_path = dest_path.replace('.md','.html')
            generate_page(src_path, template_path, dest_path, basepath)
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
            

def main():
    if sys.argv[0]:
        basepath = sys.argv[0]
    else:
        basepath = '/'
    clean_dir('docs')
    copy_static('static','docs')
    generate_pages_recursive('content','template.html','docs', basepath)
   
if __name__ == '__main__':
    main()
