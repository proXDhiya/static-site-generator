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

def main():
    source_folder = './static'
    target_folder = './public'
    clear_directory(target_folder)
    copy_recursive(source_folder, target_folder)

if __name__ == '__main__':
    main()
