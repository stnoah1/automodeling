function [] = plot3d(mat_file='../tmp/voxel.mat', rotate_num=1)
  setenv("GNUTERM", "qt")
  voxel = load(mat_file);
  voxel_each = double(squeeze(voxel.result(1, rotate_num, :, :, :)));

  p = patch(isosurface(voxel_each, 0));
  set(p, 'FaceColor', 'red', 'EdgeColor', 'none');


  daspect([1 1 1]);
  view(3)
  camlight
  lighting gouraud

end