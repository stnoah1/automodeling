import numpy as np
import scipy.io


def execute(in_mat_file, out_npz_file, num_rotate=12, res=32):
    train = scipy.io.loadmat(in_mat_file)

    # Delete extra .matfile stuff
    del train['__globals__']
    del train['__header__']
    del train['__version__']

    targets = np.asarray([], dtype=np.uint8)
    features = np.zeros((1, 1, res, res, res), dtype=np.uint8)

    # Select which classes to read in
    class_keys = sorted(train.keys())

    for i, key in enumerate(class_keys):
        targets = np.append(targets, i * np.ones(num_rotate * len(train[key]), dtype=np.uint8))
        features = np.append(
            features,
            np.reshape(train[key], (num_rotate * np.shape(train[key])[0], 1, res, res, res)),
            axis=0
        )
        if i == 0:
            features = np.delete(features, 0, axis=0)
        del train[key]
    del train

    np.savez_compressed(out_npz_file, **{'features': features, 'targets': targets})
