import _pickle as pickle
import logging
import warnings

import lasagne
import numpy as np


def load_weights(fname, l_out):
    params = lasagne.layers.get_all_params(l_out, trainable=True) + \
             [x for x in lasagne.layers.get_all_params(l_out) if x.name[-4:] == 'mean' or x.name[-7:] == 'inv_std']
    names = [par.name for par in params]
    if len(names) != len(set(names)):
        raise ValueError('need unique param names')

    param_dict = np.load(fname)
    for param in params:
        if param.name in param_dict:
            stored_shape = np.asarray(param_dict[param.name].shape)
            param_shape = np.asarray(param.get_value().shape)
            if not np.all(stored_shape == param_shape):
                warn_msg = 'shape mismatch:'
                warn_msg += '{} stored:{} new:{}'.format(param.name, stored_shape, param_shape)
                warn_msg += ', skipping'
                warnings.warn(warn_msg)
            else:
                param.set_value(param_dict[param.name])
        else:
            logging.warn('unable to load parameter {} from {}'.format(param.name, fname))
    if 'metadata' in param_dict:
        metadata = pickle.loads(param_dict['metadata'])
    else:
        metadata = {}
    return metadata
