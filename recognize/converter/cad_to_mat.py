import os
import shutil
import subprocess
from os.path import splitext

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class FileFormatError(Exception):
    pass


def execute(file, res=32, num_rotate=12):
    _, file_ext = splitext(file)
    if file_ext in ['.off', '.stl']:
        subprocess.call([
            'octave-cli',
            '--eval',
            'cd {mfile_path}; {cad_format}_to_voxel(\'{file}\', {res}, {num_rotate})'.format(
                cad_format=file_ext.split('.')[1],
                mfile_path=os.path.join(CURRENT_DIR, 'matlab'),
                file=file,
                res=res,
                num_rotate=num_rotate
            )
        ])
        return os.path.join(CURRENT_DIR, 'tmp', 'voxel.mat')
    else:
        raise FileFormatError


if __name__ == '__main__':
    execute('test_data/airplane.off')
