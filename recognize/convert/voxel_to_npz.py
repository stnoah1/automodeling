##Script for creating Modelnet40  Datasets
# A Brock, 2016

# This code, in its current form, saves an NPZ file by reading in a .mat file
# (previously prepared using the make_mats.m code) containing arrays of 
# the voxellated modelnet40 models, with 24 different rotations for each model.
# Each 5D-array is organized in the format (instance-rotations-spatialdim1-spatialdim2-spatialdim3).
# This code currently separates the rotations out such that each rotation is a separate instance, but if
# you have GPU memory to spare and are feeling masochistic, you're welcome to treat the rotations as channels
# (a la RGB in 2D imagery). I found that this didn't really change performance and just made my models take
# up more memory.
#
# This file also has commented out code which is pretty close to being able to store this data in an
# HDF5 dataset accessible by fuel, but no guarantees as I always had enough RAM available to load the
# whole dataset and didn't really need to worry about the hard-disk format.

import numpy as np
import scipy.io
train = scipy.io.loadmat('train24_32.mat')

# Delete extra .matfile stuff
del train['__globals__']
del train['__header__']
del train['__version__']

# Prepare data arrays
NUM_ROTATE = 12
RESOLUTION = 32

targets = np.asarray([], dtype=np.uint8)
features = np.zeros((1, 1, RESOLUTION, RESOLUTION, RESOLUTION), dtype=np.uint8)

# Select which classes to read in
class_keys = sorted(train.keys())

for i, key in enumerate(class_keys):
    targets = np.append(targets, i * np.ones(NUM_ROTATE * len(train[key]), dtype=np.uint8))
    features = np.append(features, np.reshape(train[key], (NUM_ROTATE * np.shape(train[key])[0], 1, RESOLUTION, RESOLUTION, RESOLUTION)), axis=0)
    if i == 0:
        features = np.delete(features, 0, axis=0)
    del train[key]
del train

np.savez_compressed('modelnet40_rot24_train.npz', **{'features': features, 'targets': targets})
