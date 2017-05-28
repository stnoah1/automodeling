import numpy as np

from recognize.classifier import run, initialize
from recognize.converter import data2npz

MODEL_NET_40_CLASS = ['airplane', 'bathtub', 'bed', 'bench', 'bookshelf', 'bottle', 'bowl', 'car', 'chair', 'cone',
                      'cup', 'curtain', 'desk', 'door', 'dresser', 'flower_pot', 'glass_box', 'guitar', 'keyboard',
                      'lamp', 'laptop', 'mantel', 'monitor', 'night_stand', 'person', 'piano', 'plant', 'radio',
                      'range_hood', 'sink', 'sofa', 'stairs', 'stool', 'table', 'tent', 'toilet', 'tv_stand', 'vase',
                      'wardrobe', 'xbox']


def get_model_info(tvars, tfuncs, data):
    npz_file = data2npz(data)

    fc_vector = run(tvars, tfuncs, npz_file)
    related_models = get_neighbor_model(fc_vector)
    confidence_rate = softmax(fc_vector)

    return {
        'class_info': [
            {'class_id': MODEL_NET_40_CLASS[index], 'confidence_rate': value}
            for index, value in enumerate(confidence_rate)
        ],
        'related_models': related_models
    }


def get_neighbor_model(fc_vector, number=20):
    related_models = [34, 22, 11, 33, 44]
    return related_models


def softmax(w, t=1.0):
    e = np.exp(np.array(w) / t)
    dist = e / np.sum(e)
    return dist


if __name__ == '__main__':
    tfuncs, tvars = initialize(model='VRN')
    print(get_model_info(tfuncs, tvars, 'test_data/airplane.off'))
