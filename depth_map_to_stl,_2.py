# -*- coding: utf-8 -*-
"""Depth map to STL, 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dttpXakpLFlKuMk8byAOl_zry5MvpCmK
"""

#@title Depth Map to STL (~2min per megapixel)

print("Depth maps only show relative depth, so the division of the maximum depth and the width of the image is needed.")
print("E.g. an object that is 10cm tall and 20cm wide, the value would be 0.5")
height_div_width = input('Enter desired value for image depth/width: ')
print('')
print("Upload depth maps:")

from google.colab import files
uploaded = files.upload()

!pip install numpy-stl
import numpy as np
from stl import mesh
import cv2

file_names = list(uploaded.keys())

for file_name in file_names:
    im = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    im_array = np.array(im) #.transpose((1, 0, 2))
    im_array = np.rot90(im_array, -1, (0,1))

    mesh_size = [im_array.shape[0],im_array.shape[1]]

    height_div_width = 0.1
    mesh_max = np.max(im_array)

    if len(im_array.shape) == 3:
        scaled_mesh = mesh_size[0] * height_div_width * im_array[:,:,0] / mesh_max
    else:
        scaled_mesh = mesh_size[0] * height_div_width * im_array / mesh_max
    # rand_mesh = np.random.rand(mesh_size[0],mesh_size[1])

    mesh_shape = mesh.Mesh(np.zeros((mesh_size[0] - 1) * (mesh_size[1] - 1) * 2, dtype=mesh.Mesh.dtype))

    for i in range(0, mesh_size[0]-1):
        for j in range(0, mesh_size[1]-1):
            mesh_num = i * (mesh_size[1]-1) + j

            mesh_shape.vectors[2 * mesh_num][2] = [i, j, scaled_mesh[i,j]]
            mesh_shape.vectors[2 * mesh_num][1] = [i, j+1, scaled_mesh[i,j+1]]
            mesh_shape.vectors[2 * mesh_num][0] = [i+1, j, scaled_mesh[i+1,j]]

            mesh_shape.vectors[2 * mesh_num + 1][0] = [i+1, j+1, scaled_mesh[i+1,j+1]]
            mesh_shape.vectors[2 * mesh_num + 1][1] = [i, j+1, scaled_mesh[i,j+1]]
            mesh_shape.vectors[2 * mesh_num + 1][2] = [i+1, j, scaled_mesh[i+1,j]]

    mesh_shape.save(str(file_name) + '.stl')
    files.download(str(file_name) + '.stl')