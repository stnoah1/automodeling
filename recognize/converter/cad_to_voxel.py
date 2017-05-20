import os
from os.path import splitext


class FileFormatError(Exception):
    pass


def execute(file, res=32, num_rotate=12):
    _, file_ext = splitext(file)
    if file_ext == '.stl':
        os.system('octave-cli --eval "cd matlab; stl_to_voxel(\'{file}\', {res}, {num_rotate})"'.format(
            file=os.path.join('..', file),
            res=res,
            num_rotate=num_rotate
        ))
    elif file_ext == '.off':
        os.system('octave-cli --eval "cd matlab; off_to_voxel(\'{file}\', {res}, {num_rotate})"'.format(
            file=os.path.join('..', file),
            res=res,
            num_rotate=num_rotate
        ))
    else:
        raise FileFormatError


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="cad file path")
    args = parser.parse_args()
    execute(str(args.file_path))
