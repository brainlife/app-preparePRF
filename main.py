#!/usr/bin/env python

# r2 + freesurfer files => r2 overlay information (25 MB)
# get task id from config.json => send task id to ui-3dsurfaces
# ui-3dsurfaces gets task id from url then grabs 25 MB of data...
# download output then reupload?

# output config for ui-3dsurfaces in the following format:
# (output.json)
# {
#   surfaces: [{
#       "name": ...,
#       "filename": ...,
#       "filetype": "vtk",
#       "color": ...,
#       "left": ...,
#       "right": ...,
#   }],
#   color_maps: {
#       "freesurfer/surf/lh.inflated.vtk": {
#           "0": .06112977,
#           ...
#       },
#       ...
#   },
#   morph_maps: {
#       "freesurfer/surf/lh.inflated.vtk": {
#           "0": [128, 33, 37],
#           ...
#       },
#       ...
#   }
# }
# 
# 
# ...to be used as local storage config for ui-3dsurfaces

def inside_bounds(x, y, z, shape):
    shape_x, shape_y, shape_z = shape
    return (x >= 0 and y >= 0 and z >= 0
            and x < shape_x and y < shape_y and z < shape_z)

import nibabel as nib
import os
import json
import loader
import nibabel as nib
import numpy as np

with open('config.json') as config_json:
    config = json.load(config_json)

# loading r2
r2 = nib.load('input/prf/r2.fixed.nii')
r2_data = r2.get_fdata()
xform = np.mat(r2.get_sform())
inv_xform = np.linalg.inv(xform)

# loading config surfaces
lh_pial_path = os.path.join(config['freesurfer'], "surf/lh.pial.vtk")
rh_pial_path = os.path.join(config['freesurfer'], "surf/rh.pial.vtk")

lh_pial = loader.load_vtk(lh_pial_path)
rh_pial = loader.load_vtk(rh_pial_path)
lh_inflated = loader.load_vtk(os.path.join(config['freesurfer'], "surf/lh.inflated.vtk"))
rh_inflated = loader.load_vtk(os.path.join(config['freesurfer'], "surf/rh.inflated.vtk"))
lh_white = loader.load_vtk(os.path.join(config['freesurfer'], "surf/lh.white.vtk"))
rh_white = loader.load_vtk(os.path.join(config['freesurfer'], "surf/rh.white.vtk"))

surfaces = []
color_maps = dict()
morph_maps = dict()

color_maps[lh_pial_path] = dict()
color_maps[rh_pial_path] = dict()

morph_maps[lh_pial_path] = dict()
morph_maps[rh_pial_path] = dict()

# write left-hand side information
for i in range(len(lh_pial)):
    lh_x = (lh_white[i][0] + lh_pial[i][0]) / 2
    lh_y = (lh_white[i][1] + lh_pial[i][1]) / 2
    lh_z = (lh_white[i][2] + lh_pial[i][2]) / 2
    
    lh_r2_xyz = np.matmul(inv_xform, np.mat([[lh_x], [lh_y], [lh_z], [1]]))
    x, y, z, w = [int(v) for v in np.round(lh_r2_xyz.flatten()).tolist()[0]]
    
    if inside_bounds(x, y, z, r2_data.shape) and np.isfinite(r2_data[x, y, z]):
        color_maps[lh_pial_path][i] = r2_data[x, y, z]
    morph_maps[lh_pial_path][i] = lh_inflated[i]

# write right-hand side information
for i in range(len(rh_pial)):
    rh_x = (rh_white[i][0] + rh_pial[i][0]) / 2
    rh_y = (rh_white[i][1] + rh_pial[i][1]) / 2
    rh_z = (rh_white[i][2] + rh_pial[i][2]) / 2
    
    rh_r2_xyz = np.matmul(inv_xform, np.mat([[rh_x], [rh_y], [rh_z], [1]]))
    x, y, z, w = [int(v) for v in np.round(rh_r2_xyz.flatten()).tolist()[0]]
    
    if inside_bounds(x, y, z, r2_data.shape) and np.isfinite(r2_data[x, y, z]):
        color_maps[rh_pial_path][i] = r2_data[x, y, z]
    morph_maps[rh_pial_path][i] = rh_inflated[i]

output = { 'surfaces': surfaces, 'color_maps': color_maps, 'morph_maps': morph_maps }

with open('output.json', 'w+') as output_json:
    output_json.write(json.dumps(output))