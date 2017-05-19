import os
from os.path import splitext


class FileFormatError(Exception):
    pass


def execute(file_path):
    _, file_ext = splitext(file_path)
    if file_ext == '.stl':
        os.system('octave-cli --eval "cd stl; stl_to_voxel(\'{file_path}\')"'.format(file_path=os.path.join('..', file_path)))
    elif file_ext == '.off':
        os.system('octave-cli --eval "cd off; off_to_voxel(\'{file_path}\')"'.format(file_path=os.path.join('..', file_path)))
    else:
        raise FileFormatError


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="cad file path")
    args = parser.parse_args()
    execute(args.file_path)
