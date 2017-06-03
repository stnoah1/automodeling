import lasagne
import numpy as np
import os
import theano
import theano.tensor as T

# Define the testing functions
from recognize.classifier.utils import checkpoints

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def classifying_function(cfg, model):
    # print('CLASSIFYING_FUNCTION: Input Array')
    X = T.TensorType('float32', [False] * 5)('X')

    # print('CLASSIFYING_FUNCTION: Shared Variable for input array')
    X_shared = lasagne.utils.shared_empty(5, dtype='float32')

    # print('CLASSIFYING_FUNCTION: Output layer')
    l_out = model['l_out']

    # print('CLASSIFYING_FUNCTION: Batch Parameters')
    batch_index = T.iscalar('batch_index')
    test_batch_slice = slice(batch_index * cfg['n_rotations'], (batch_index + 1) * cfg['n_rotations'])

    # print('CLASSIFYING_FUNCTION: Get output')
    y_hat_deterministic = lasagne.layers.get_output(l_out, X, deterministic=True)

    # print('CLASSIFYING_FUNCTION: Compile Functions')
    fc_vector = theano.function([batch_index], [T.sum(y_hat_deterministic, axis=0)], givens={
        X: X_shared[test_batch_slice]
    })
    # print('CLASSIFYING_FUNCTION: Compiling finished')
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
    weights_fname = os.path.join(CURRENT_DIR, 'models', '{model}.npz'.format(model=model))

    # Get Model
    model = config_module.get_model()

    # Compile functions
    # print('INITIALIZE: Compiling theano functions...!!')
    tfuncs, tvars, model = classifying_function(cfg, model)

    # print('INITIALIZE: Load weights')
    checkpoints.load_weights(weights_fname, model['l_out'])
    # print('INITIALIZE: All weights loaded')
    return tfuncs, tvars


def run(tvars, tfuncs, data_path):
    # print('RUN: np x loading started')
    xt = np.asarray(np.load(data_path)['features'], dtype=np.float32)
    x_shared = np.asarray(xt[0:12, :, :, :, :], dtype=np.float32)

    # print('RUN: Prepare data')
    tvars['X_shared'].set_value(4.0 * x_shared - 1.0, borrow=True)
    # print('RUN: Prepare data finished')
    return tfuncs['fc_vector'](0)[0].tolist()


if __name__ == '__main__':
    tfuncs, tvars = initialize(model='VRN')
    run(tfuncs, tvars, '../converter/tmp/voxel.npz')
