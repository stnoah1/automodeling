from os.path import splitext


class FileFormatError(Exception):
    pass


def execute(file_path):
    npz_file_path = converter(file_path)
    model_class, fc_vector = classifier(npz_file_path)
    neighbor_model_list = get_neighbor_model(fc_vector)
    # remove temporary(npz, mat) file
    return model_class, fc_vector


def init_octave():
    # octave-cli pkg load image
    pass


def converter(file_path):
    file_ext = splitext(file_path)
    if file_ext == 'stl':
        stl_to_voxel(file_path)
    elif file_ext == 'off':
        init_octave()
        off_to_voxel(file_path)
    else:
        raise FileFormatError


def stl_to_voxel(file_path):
    # octave-cli stl_to_voxel
    pass


def off_to_voxel(file_path):
    # octave-cli off_to_voxel
    pass


def classifier(npz_file_path):
    return model_class, fc_vector


def get_neighbor_model(fc_vector):
    pass
