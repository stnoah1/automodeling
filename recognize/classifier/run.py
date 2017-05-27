###
# Discriminative Voxel-Based ConvNet Training Function
# A Brock, 2016


import math

import theano
import lasagne
import numpy as np
import theano.tensor as T

# Define the testing functions
from recognize.classifier.utils import checkpoints


def make_testing_functions(cfg, model):
    # Input Array
    X = T.TensorType('float32', [False] * 5)('X')

    # Shared Variable for input array
    X_shared = lasagne.utils.shared_empty(5, dtype='float32')

    # Class Vector
    y = T.TensorType('int32', [False] * 1)('y')

    # Shared Variable for class vector
    y_shared = lasagne.utils.shared_empty(1, dtype='float32')

    # Output layer
    l_out = model['l_out']

    # Batch Parameters
    batch_index = T.iscalar('batch_index')
    test_batch_slice = slice(batch_index * cfg['n_rotations'], (batch_index + 1) * cfg['n_rotations'])

    # Get output
    y_hat_deterministic = lasagne.layers.get_output(l_out, X, deterministic=True)

    # Average across rotation examples
    pred = T.argmax(T.sum(y_hat_deterministic, axis=0))

    # Get error rate
    classifier_test_error_rate = T.cast(T.mean(T.neq(pred, T.mean(y, dtype='int32'))), 'float32')

    # Compile Functions
    test_error_fn = theano.function([batch_index], [classifier_test_error_rate, pred], givens={
        X: X_shared[test_batch_slice],
        y: T.cast(y_shared[test_batch_slice], 'int32')
    })
    tfuncs = {'test_function': test_error_fn}
    tvars = {'X': X,
             'y': y,
             'X_shared': X_shared,
             'y_shared': y_shared,
             }
    return tfuncs, tvars, model


# Main Function
class WrongModelError(object):
    pass


def main(data_path, model='VRN'):
    if model == 'VRN':
        from recognize.classifier.models import VRN as config_module
    else:
        raise WrongModelError

    cfg = config_module.CONFIG

    # Find weights file
    weights_fname = 'models/{model}.npz'.format(model=model)

    # Get Model
    model = config_module.get_model()

    # Compile functions
    print('Compiling theano functions...')
    tfuncs, tvars, model = make_testing_functions(cfg, model)

    # Load weights
    checkpoints.load_weights(weights_fname, model['l_out'])

    xt = np.asarray(np.load(data_path)['features'], dtype=np.float32)
    yt = np.asarray(np.load(data_path)['targets'], dtype=np.float32)

    n_rotations = cfg['n_rotations']

    x_shared = np.asarray(xt[0:n_rotations, :, :, :, :], dtype=np.float32)
    y_shared = np.asarray(yt[0:n_rotations], dtype=np.float32)

    # Prepare data
    tvars['X_shared'].set_value(4.0 * x_shared - 1.0, borrow=True)
    tvars['y_shared'].set_value(y_shared, borrow=True)

    # Loop across batches!

    [_, pred] = tfuncs['test_function'](0)
    print(pred)


if __name__ == '__main__':
    main('../converter/tmp/voxel.npz')
