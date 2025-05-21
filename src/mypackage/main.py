from mypackage.transformers.transformer import generate_page
import shutil
import os


def clear_directory(path):
    if os.path.exists(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
    else:
        os.makedirs(path)


def copy_recursive(src, dest):
    for item in os.listdir(src):
        s_item = os.path.join(src, item)
        d_item = os.path.join(dest, item)
        if os.path.isdir(s_item):
            shutil.copytree(s_item, d_item)
        else:
            shutil.copy2(s_item, d_item)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                content_path = os.path.join(root, file)
                relative_path = os.path.relpath(content_path, dir_path_content)
                dest_html_path = os.path.splitext(relative_path)[0] + '.html'
                dest_path = os.path.join(dest_dir_path, dest_html_path)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(content_path, template_path, dest_path)


def main():
    source_folder = './static'
    target_folder = './public'
    clear_directory(target_folder)
    copy_recursive(source_folder, target_folder)

    template_path = './template.html'
    generate_pages_recursive('./content', template_path, target_folder)


if __name__ == '__main__':
    main()
