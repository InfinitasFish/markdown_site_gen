import os
import sys
import shutil

sys.path.append('../site_gen')
from root import ROOT_DIR


def copy_source_dir_to_destination(source, destination):
    full_source_path = os.path.join(ROOT_DIR, source)
    if not os.path.exists(full_source_path):
        return
    full_destination_path = os.path.join(ROOT_DIR, destination)

    if not os.path.isdir(full_source_path):
        raise ValueError(f'source isnt a dir in copy_source_dir_to_destination(): {full_source_path}')

    if not os.path.exists(full_destination_path):
        os.mkdir(full_destination_path)
    else:
        for file in os.listdir(full_destination_path):
            file_path = os.path.join(full_destination_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # copying
    for file in os.listdir(full_source_path):
        source_file_path = os.path.join(full_source_path, file)
        if os.path.isdir(source_file_path):
            destination_dir = os.path.join(full_destination_path, file)
            copy_source_dir_to_destination(source_file_path, destination_dir)
        else:
            destination_file = os.path.join(full_destination_path, file)
            shutil.copyfile(source_file_path, destination_file)


# test
if __name__ == '__main__':
    source = os.path.join(ROOT_DIR, 'static')
    destination = os.path.join(ROOT_DIR, 'public_test')
    copy_source_dir_to_destination(source, destination)