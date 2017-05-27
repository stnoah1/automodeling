import numpy as np
import os

from recognize.classifier import run
from recognize.converter import cad_to_mat, mat_to_npz


def get_model_info(data):
    # file = data2stl(data)
    # mat_file_path = cad_to_mat.execute(file)
    # npz_file_path = mat_file_path.split('.')[0] + '.npz'

    # mat_to_npz.execute(in_mat_file=mat_file_path, out_npz_file=npz_file_path)
    fc_vector = run.main()
    confidence_rate = softmax(fc_vector)
    related_models = get_neighbor_model(fc_vector)

    # remove temporary(npz, mat) file
    # os.remove(mat_file_path)
    # os.remove(npz_file_path)

    return {
        'class_info': [
            {'class_id': index, 'confidence_rate': value} for index, value in enumerate(confidence_rate)
        ],
        'related_models': related_models
    }


def get_neighbor_model(fc_vector):
    related_models = [34, 22, 11, 33, 44]
    return related_models


# db를 npz 파일로 가지고 있기


def data2stl(data):
    # stl 을 off 으로 변경하는 것이 나을 수도 있음 속도 비교해보기
    stl_path = 'test_data/chair.off'
    return stl_path


def softmax(w, t=1.0):
    e = np.exp(np.array(w) / t)
    dist = e / np.sum(e)
    return dist


if __name__ == '__main__':
    print(get_model_info('test_data/airplane.off'))
