import os

import numpy as np

from recognize.classifier import run, initialize
from recognize.converter import off2mat, mat2npz, stl2off


def create_fc_vector_npz(data_path, tfuncs, tvars):
    """
    stl 데이터가 뉴럴 네트워크를 거쳐 출력된 fc_vector를 stl 파일 이름을 dictionary의 key로 하여 .npz파일에 저장
    :param data_path: ModelNet .stl 파일 경로
    """
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


def stl2off_meshconv(file_path):
    """
    meshconv를 이용해 off 파일을 stl 파일로 변환 시켜주기 위한 .bat 파일 생성
    meshconv-link : http://www.patrickmin.com/meshconv/
    :param file_path: ModelNet 파일 위치
    """
    with open("off_to_stl.bat", 'w') as f:
        for cad_class in os.listdir(file_path):
            for sub_path in ['train', 'test']:
                class_folder = os.path.join(file_path, cad_class, sub_path)
                for off_file in os.listdir(class_folder):
                    os.path.join(class_folder, off_file)
                    f.write("meshconv -c stl -tri {} \n".format(os.path.join(class_folder, off_file)))


if __name__ == '__main__':
    data_path = '/Users/noah/Projects/automodeling/ModelNet40_stl'
    tfuncs, tvars = initialize(model='VRN')
    create_fc_vector_npz(tfuncs, tvars, data_path)
