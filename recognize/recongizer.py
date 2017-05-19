from recognize import voxelise


def execute(file_path):
    voxelise.converter.execute(file_path)
    # model_class, fc_vector = classifier(npz_file_path)
    # neighbor_model_list = get_neighbor_model(fc_vector)
    # remove temporary(npz, mat) file


def classifier(npz_file_path):
    pass


def get_neighbor_model(fc_vector):
    pass
