import lasagne
import numpy as np
import os
import theano
import theano.tensor as T

# Define the testing functions
from recognize.classifier.utils import checkpoints

WORKING_DIR = os.getcwd()


def classifing_function(cfg, model):
    # Input Array
    X = T.TensorType('float32', [False] * 5)('X')

    # Shared Variable for input array
    X_shared = lasagne.utils.shared_empty(5, dtype='float32')

    # Output layer
    l_out = model['l_out']

    # Batch Parameters
    batch_index = T.iscalar('batch_index')
    test_batch_slice = slice(batch_index * cfg['n_rotations'], (batch_index + 1) * cfg['n_rotations'])

    # Get output
    y_hat_deterministic = lasagne.layers.get_output(l_out, X, deterministic=True)

    # Compile Functions
    fc_vector = theano.function([batch_index], [T.sum(y_hat_deterministic, axis=0)], givens={
        X: X_shared[test_batch_slice]
    })

    tfuncs = {'fc_vector': fc_vector}
    tvars = {'X': X,
             'X_shared': X_shared,
             }
    return tfuncs, tvars, model


# Main Function
class WrongModelError(object):
    pass


def initialize(model='VRN'):
    if model == 'VRN':
        from recognize.classifier.models import VRN as config_module
    else:
        raise WrongModelError

    cfg = config_module.CONFIG

    # Find weights file
    weights_fname = os.path.join(WORKING_DIR, 'classifier', 'models', '{model}.npz'.format(model=model))

    # Get Model
    model = config_module.get_model()

    # Compile functions
    print('Compiling theano functions...!!')
    tfuncs, tvars, model = classifing_function(cfg, model)

    # Load weights
    checkpoints.load_weights(weights_fname, model['l_out'])

    return tfuncs, tvars


def run(tvars, tfuncs, data_path):
    xt = np.asarray(np.load(data_path)['features'], dtype=np.float32)
    x_shared = np.asarray(xt[0:12, :, :, :, :], dtype=np.float32)

    # Prepare data
    tvars['X_shared'].set_value(4.0 * x_shared - 1.0, borrow=True)

    return tfuncs['fc_vector'](0)[0].tolist()


if __name__ == '__main__':
    tfuncs, tvars = initialize(model='VRN')
    run(tfuncs, tvars, '../converter/tmp/voxel.npz')
