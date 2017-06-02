import os
import uuid
from os.path import splitext

import numpy as np
import scipy.io
from oct2py import octave
from trimesh import load_mesh
from trimesh.io.export import export_off

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOLUTION = 32
NUM_ROTATE = 12


class FileFormatError(Exception):
    pass


def data2stl(data, stl_file=os.path.join(CURRENT_DIR, 'tmp', '{stl_file}.stl'.format(stl_file=str(uuid.uuid4())))):
    with open(stl_file, "w") as f:
        f.write(data)
    return stl_file


def stl2off(stl_file, off_file=None, delete_file=True):
    file_format_check(stl_file, '.stl')
    if off_file is None:
        off_file = stl_file.replace('.stl', '.off')
    mesh = load_mesh(stl_file)
    off_data = export_off(mesh)
    with open(off_file, 'w') as f:
        f.write(off_data)
    if delete_file:
        os.remove(stl_file)
    return off_file


def off2mat(off_file, res=RESOLUTION, num_rotate=NUM_ROTATE, delete_file=True):
    file_format_check(off_file, '.off')
    octave.addpath(os.path.join(CURRENT_DIR, 'utills'))
    octave.eval('clear', 'all')
    mat_file = octave.eval(
        'off2voxel(\'{off_file}\', {res}, {num_rotate});'.format(
            off_file=off_file,
            res=res,
            num_rotate=num_rotate
        )
    )
    if delete_file:
        os.remove(off_file)
    return mat_file


def mat2npz(mat_file, npz_file=None, res=RESOLUTION, num_rotate=NUM_ROTATE, delete_file=True):
    file_format_check(mat_file, '.mat')
    if npz_file is None:
        npz_file = mat_file.replace('.mat', '.npz')

    train = scipy.io.loadmat(mat_file)

    if delete_file:
        os.remove(mat_file)

    # Delete extra .matfile stuff
    del train['__globals__']
    del train['__header__']
    del train['__version__']

    features = np.zeros((1, 1, res, res, res), dtype=np.uint8)

    # Select which classes to read in
    class_keys = sorted(train.keys())

    for i, key in enumerate(class_keys):
        features = np.append(
            features,
            np.reshape(train[key], (num_rotate * np.shape(train[key])[0], 1, res, res, res)),
            axis=0
        )
        if i == 0:
            features = np.delete(features, 0, axis=0)
        del train[key]
    del train

    np.savez_compressed(npz_file, **{'features': features})
    return npz_file


def data2npz(stl_data):
    stl_file = data2stl(stl_data)
    off_file = stl2off(stl_file)
    mat_file = off2mat(off_file)
    return mat2npz(mat_file)


def file_format_check(file, file_format):
    _, file_ext = splitext(file)
    if file_ext.lower() != file_format.lower():
        raise FileFormatError


if __name__ == '__main__':
    import time

    tic = time.clock()
    stl_file = os.path.join(CURRENT_DIR, 'tmp', 'airplane_0004.stl')
    off_file = stl2off(stl_file, delete_file=False)
    print('off conversion success')
    mat_file = off2mat(off_file, delete_file=False)
    print('mat conversion success')
    mat2npz(mat_file, delete_file=False)
    print('npz conversion success')
    toc = time.clock()
    print(toc - tic)
