import os
import time
from pprint import pprint

import numpy as np

from recognize.classifier import run, initialize
from recognize.converter import to_npz

MODEL_NET_40_CLASS = ['airplane', 'bathtub', 'bed', 'bench', 'bookshelf', 'bottle', 'bowl', 'car', 'chair', 'cone',
                      'cup', 'curtain', 'desk', 'door', 'dresser', 'flower_pot', 'glass_box', 'guitar', 'keyboard',
                      'lamp', 'laptop', 'mantel', 'monitor', 'night_stand', 'person', 'piano', 'plant', 'radio',
                      'range_hood', 'sink', 'sofa', 'stairs', 'stool', 'table', 'tent', 'toilet', 'tv_stand', 'vase',
                      'wardrobe', 'xbox']

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def get_model_info(tfuncs, tvars, stl_data):
    # print("GET_MODEL_INFO: npz_file")
    npz_file = to_npz(stl_data, rotate=True)
    # print("GET_MODEL_INFO: fc_vector")
    fc_vector = run(tvars, tfuncs, npz_file)
    # print("GET_MODEL_INFO: related_models")
    related_models = get_related_models(fc_vector)
    # print("GET_MODEL_INFO: confidence_rate")
    confidence_rate = softmax(fc_vector)
    # print("GET_MODEL_INFO: class_info")
    class_info = sorted(
        [
            {'class_id': MODEL_NET_40_CLASS[index], 'confidence_rate': value}
            for index, value in enumerate(confidence_rate)
        ],
        key=lambda k: k['confidence_rate'],
        reverse=True)
    return {
        'class_info': class_info,
        'related_models': related_models
    }


def get_related_models(fc_vector, data_path=os.path.join(CURRENT_DIR, 'fc_vector_set.npz'), num_model=20):
    fc_vector_data = np.load(data_path)
    l2_set = {}
    for key, value in fc_vector_data.items():
        l2 = np.linalg.norm(np.array(fc_vector) - np.array(value))
        l2_set.update({key: l2})
    related_model_list = sorted(l2_set, key=l2_set.get)[:num_model]
    return related_model_list


def softmax(w, t=1.0):
    e = np.exp(np.array(w) / t)
    dist = e / np.sum(e)
    return dist


def test(*path):
    start = time.time()
    with open(os.path.join(*path), 'r') as f:
        data = f.read()
    pprint(get_model_info(tfuncs, tvars, data))
    end = time.time()
    print("MAIN: Run time: {}".format(str(end - start)))


if __name__ == '__main__':
    tfuncs, tvars = initialize(model='VRN')
    print('MAIN: Initializing finished')
    test(CURRENT_DIR, 'converter', 'tmp', 'nice_chair.txt')
    test(CURRENT_DIR, 'converter', 'tmp', 'nice_chair.txt')
