###
# Discriminative Voxel-Based ConvNet Training Function
# A Brock, 2016


import argparse
import math

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

    # Output layer
    l_out = model['l_out']

    # Batch Parameters
    batch_index = T.iscalar('batch_index')
    test_batch_slice = slice(batch_index * cfg['n_rotations'], (batch_index + 1) * cfg['n_rotations'])
    test_batch_i = batch_index

    # Get output
    y_hat_deterministic = lasagne.layers.get_output(l_out, X, deterministic=True)

    # Average across rotation examples
    pred = T.argmax(T.sum(y_hat_deterministic, axis=0))

    # Compile Functions
    tvars = {'X': X,
             'X_shared': X_shared,
             }
    return l_out, pred, tvars, model


# Main Function
class WrongModelError(object):
    pass


def main(data_path, model='VRN'):
    if model == 'VRN':
        from recognize.classifier.models import VRN as config_module
    else:
        raise WrongModelError

    # Load config module
    cfg = config_module.CONFIG

    # Find weights file
    weights_fname = 'models/{model}.npz'.format(model=model)

    # Get Model
    model = config_module.get_model()

    # Compile functions
    print('Compiling theano functions...')
    l_out, pred, tvars, model = make_testing_functions(cfg, model)

    # Load weights
    metadata = checkpoints.load_weights(weights_fname, model['l_out'])

    # Check if previous best accuracy is in metadata from previous tests
    best_acc = metadata['best_acc'] if 'best_acc' in metadata else 0
    print('best accuracy = ' + str(best_acc))

    print('Testing...')
    itr = 0

    # Load testing data into memory
    xt = np.asarray(np.load(data_path)['features'], dtype=np.float32)

    # Get number of rotations to average across. If you want this to be different from
    # the number of rotations specified in the config file, make sure to change the 
    # indices of the test_batch_slice variable above, as well as which data file
    # you're reading from.
    n_rotations = cfg['n_rotations']

    # Confusion Matrix: Currently not implemented as it doesn't print prettily,
    # but easy to add in by uncommenting some of the commented lines in the loop.
    confusion_matrix = np.zeros((40, 40), dtype=np.int)

    # Determine chunk size
    test_chunk_size = n_rotations * cfg['batches_per_chunk']

    # Determine number of chunks
    num_test_chunks = int(math.ceil(float(len(xt)) / test_chunk_size))

    # Total number of test batches. Note that we're treating all the rotations
    # of a single instance as a single batch. There's definitely a more efficient
    # way to do this, and you'll want to be more efficient if you implement this in 
    # a validation loop, but testing should be infrequent enough that the extra few minutes
    # this costs is irrelevant.
    num_test_batches = int(math.ceil(float(len(xt)) / float(n_rotations)))

    # Prepare test error  
    test_class_error = []

    # Initialize test iteration counter
    test_itr = 0

    # Loop across chunks!
    for chunk_index in range(num_test_chunks):

        # Define upper index of chunk
        upper_range = min(len(yt), (chunk_index + 1) * test_chunk_size)

        # Get chunks
        x_shared = np.asarray(xt[chunk_index * test_chunk_size:upper_range, :, :, :, :], dtype=np.float32)

        # Get number of batches for this chunk
        num_batches = len(x_shared) // n_rotations

        # Prepare data
        tvars['X_shared'].set_value(4.0 * x_shared - 1.0, borrow=True)

        # Loop across batches!
        for bi in range(num_batches):
            # Increment test iteration counter
            test_itr += 1

            # Test!
            [batch_test_class_error, pred] = tfuncs['test_function'](bi)

            # Record test results
            test_class_error.append(batch_test_class_error)

            # Optionally, update the confusion matrix
            # confusion_matrix[pred,int(yt[cfg['n_rotations']*test_itr])]+=1

    # Optionally, print confusion matrix
    # print(confusion_matrix)

    # Get total accuracy
    t_class_error = 1 - float(np.mean(test_class_error))
    print('Test accuracy is: ' + str(t_class_error))

    # Optionally save best accuracy
    # if t_class_error>best_acc:
    # best_acc = t_class_error
    # checkpoints.save_weights(weights_fname, models['l_out'],
    # {'best_acc':best_acc})


if __name__ == '__main__':
    main('recognize/converter/tmp/voxel.npz', 'models/VRN.py')
