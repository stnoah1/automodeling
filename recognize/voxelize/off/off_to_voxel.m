res = 32num_rotations = 12file_path =;[vertices, faces] = read_off(file_path);FV.faces = faces';for i = 1:num_rotations    theta = 2*pi*(j-1)/num_rotations;    rot_mat=[cos(theta) sin(theta) 0;-sin(theta) cos(theta) 0; 0 0 1];    FV.vertices = (rot_mat*vertices)';    result = (1,i,:,:,:)=logical(polygon2voxel(FV,[res, res, res],'auto'));endresult.save('voxel.mat')