import os

import numpy as np

from recognize.classifier import run, initialize
from recognize.converter import off2mat, mat2npz, stl2off


def create_fc_vector_npz(data_path, tfuncs, tvars):

    npz_dict = {}
    for cad_class in os.listdir(data_path):
        class_folder = os.path.join(data_path, cad_class)
        for stl_file_name in os.listdir(class_folder):
            stl_file = os.path.join(class_folder, stl_file_name)
            off_file = stl2off(stl_file)
            mat_file = off2mat(off_file)
            npz_file = mat2npz(mat_file)
            fc_vector = run(tvars, tfuncs, npz_file)
            npz_dict.update({stl_file_name.split('.')[0]: fc_vector})
            print({stl_file_name.split('.')[0]: fc_vector})
    np.savez_compressed('fc_vector_set.npz', **npz_dict)


if __name__ == '__main__':
    data_path = '/Users/noah/Projects/automodeling/ModelNet40_stl'
    tfuncs, tvars = initialize(model='VRN')
    create_fc_vector_npz(tfuncs, tvars, data_path)
