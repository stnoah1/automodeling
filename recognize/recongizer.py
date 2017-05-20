from recognize.classifier import test
from recognize.converter import cad_to_voxel, voxel_to_npz


def execute(file):
    mat_file_path = cad_to_voxel.execute(file)
    npz_file_path = 'npz_file_path'
    voxel_to_npz.execute(mat_file_path, npz_file_path)
    # test.main()


    # model_class, fc_vector = classifier(npz_file_path)
    # neighbor_model_list = get_neighbor_model(fc_vector)
    # remove temporary(npz, mat) file


def classifier(npz_file_path):
    pass


def get_neighbor_model(fc_vector):
    # db를 npz 파일로 가지고 있기
    pass
