import os
import shutil

def copystatic(source_dir, destination_dir):
    if not os.path.isdir(source_dir):
        raise Exception(f'Error: "{source_dir}" is not a directory')

    source_dir_abs = os.path.abspath(source_dir)
    destination_dir_abs = os.path.abspath(destination_dir)

    if os.path.exists(destination_dir_abs):
        shutil.rmtree(destination_dir_abs)
    os.mkdir(destination_dir_abs)

    _copy_recursively(source_dir_abs, destination_dir_abs)

def _copy_recursively(source_dir, destination_dir):
    with os.scandir(source_dir) as entries:
        for entry in entries:
            if entry.is_file():
                shutil.copyfile(os.path.join(source_dir, entry.name), os.path.join(destination_dir, entry.name))
                print(f'The file {entry.name} has been copied to {destination_dir}')
            else:
                os.mkdir(os.path.join(destination_dir, entry.name))
                print(f'The directory {entry.name} has been created in {destination_dir}')
                _copy_recursively(os.path.join(source_dir, entry.name), os.path.join(destination_dir, entry.name))
