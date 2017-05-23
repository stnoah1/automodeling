import os

from recognize.converter import cad_to_mat, mat_to_npz


def execute(file):
    mat_file_path = cad_to_mat.execute(file)
    npz_file_path = mat_file_path.split('.')[0] + '.npz'
    mat_to_npz.execute(in_mat_file=mat_file_path, out_npz_file=npz_file_path)
    # test.main()

    # model_class, fc_vector = classifier(npz_file_path)
    # neighbor_model_list = get_neighbor_model(fc_vector)

    # remove temporary(npz, mat) file
    # os.remove(mat_file_path)
    # os.remove(npz_file_path)


def get_neighbor_model(fc_vector):
    # db를 npz 파일로 가지고 있기
    pass


if __name__ == '__main__':
    execute('test_data/airplane.off')
