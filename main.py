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

import os
import json
import loader
import nibabel as nib
import numpy as np

def inside_bounds(x, y, z, shape):
    shape_x, shape_y, shape_z = shape
    return (x >= 0 and y >= 0 and z >= 0
            and x < shape_x and y < shape_y and z < shape_z)

def weight2hsv(weight):
    r = 0.0
    g = 0.0
    b = 0.0
    
    weight = float(weight)
    if weight < 1.0/6.0:
        r = 1.0
        g = weight * 6.0
    elif weight < 2.0/6.0:
        r = 1.0 - (weight - 1.0/6.0) * 6.0
        g = 1.0
    elif weight < 3.0/6.0:
        g = 1.0
        b = (weight - 2.0/6.0) * 6.0
    elif weight < 4.0/6.0:
        g = 1.0 - (weight - 3.0/6.0) * 6.0
        b = 1.0
    elif weight < 5.0/6.0:
        r = (weight - 4.0/6.0) * 6.0
        b = 1.0
    else:
        r = 1.0
        b = 1.0 - (weight - 5.0/6.0) * 6.0
    
    return (r, g, b)

def weight2heat(weight):
    r = 0.0
    g = 0.0
    b = 0.0
    
    weight = float(weight)
    if weight < 1.0/3.0:
        r = weight * 3.0
    elif weight < 2.0/3.0:
        r = 1.0
        g = (weight - 1.0/3.0) * 3.0
    else:
        r = 1.0
        g = 1.0
        b = (weight - 2.0/3.0) * 3.0
        if (b > 1.0):
            b = 1.0
    
    return (r, g, b)

with open('config.json') as config_json:
    config = json.load(config_json)

# loading r2
bold = nib.load(config['task'])
r2 = nib.load(os.path.join(config['prf'], 'r2.nii'))
r2.set_sform(bold.get_sform())
r2.set_qform(bold.get_qform())

r2_data = r2.get_fdata()

# load everything
lh_pial = loader.load_vtk('surfaces/lh.pial.vtk')
rh_pial = loader.load_vtk('surfaces/rh.pial.vtk')

lh_white = loader.load_vtk('surfaces/lh.white.vtk')
rh_white = loader.load_vtk('surfaces/rh.white.vtk')

lh_inflated = loader.load_vtk('surfaces/lh.inflated.vtk')
rh_inflated = loader.load_vtk('surfaces/rh.inflated.vtk')

# get inverse xform 
inv_xform = np.linalg.inv(r2.get_sform())

lh_surface = {
    "left": True,
    "name": "Left Pial Surface",
    "vcolor": [],
    "filename": "lh.pial.vtk",
    "filetype": "vtk",
    "morphTarget": "lh.inflated.vtk"
}
rh_surface = {
    "right": True,
    "name": "Right Pial Surface",
    "vcolor": [],
    "filename": "rh.pial.vtk",
    "filetype": "vtk",
    "morphTarget": "rh.inflated.vtk"
}

for i in range(len(lh_pial)):
    lh_inflated[i][0] -= 60
    # x = (lh_pial[i][0] + lh_white[i][0]) * .5
    # y = (lh_pial[i][1] + lh_white[i][1]) * .5
    # z = (lh_pial[i][2] + lh_white[i][2]) * .5
    x = lh_pial[i][0]
    y = lh_pial[i][1]
    z = lh_pial[i][2]
    
    r2_coord = np.matmul(inv_xform, np.mat([[x], [y], [z], [1]]))
    coords_flat = [round(x) for x in r2_coord.flatten().tolist()[0]]
    
    color = 0x808080
    if inside_bounds(coords_flat[0], coords_flat[1], coords_flat[2], r2.shape):
        r2_value = float(r2_data[coords_flat[0], coords_flat[1], coords_flat[2]])
        
        if np.isfinite(r2_value):
            r2_r, r2_g, r2_b = weight2heat(r2_value)
            color = (int(r2_r * 255.0) << 16) + (int(r2_g * 255.0) << 8) + int(r2_b * 255.0)
    
    lh_surface['vcolor'].append(color)

for i in range(len(rh_pial)):
    rh_inflated[i][0] += 60
    # x = (rh_pial[i][0] + rh_white[i][0]) * .5
    # y = (rh_pial[i][1] + rh_white[i][1]) * .5
    # z = (rh_pial[i][2] + rh_white[i][2]) * .5
    x = rh_pial[i][0]
    y = rh_pial[i][1]
    z = rh_pial[i][2]
    
    r2_coord = np.round(np.matmul(inv_xform, np.mat([[x], [y], [z], [1]])))
    coords_flat = [round(x) for x in r2_coord.flatten().tolist()[0]]
    
    color = 0x808080
    if inside_bounds(coords_flat[0], coords_flat[1], coords_flat[2], r2.shape):
        r2_value = float(r2_data[coords_flat[0], coords_flat[1], coords_flat[2]])
        
        if np.isfinite(r2_value):
            r2_r, r2_g, r2_b = weight2heat(r2_value)
            color = (int(r2_r * 255.0) << 16) + (int(r2_g * 255.0) << 8) + int(r2_b * 255.0)
    
    rh_surface['vcolor'].append(color)

loader.update_vtk('surfaces/lh.inflated.vtk', lh_inflated)
loader.update_vtk('surfaces/rh.inflated.vtk', rh_inflated)

surfaces = [lh_surface, rh_surface, {
    "left": True,
    "name": "Left Inflated Surface",
    "filename": "lh.inflated.vtk",
    "filetype": "vtk",
    "visible": False
}, {
    "right": True,
    "name": "Right Inflated Surface",
    "filename": "rh.inflated.vtk",
    "filetype": "vtk",
    "visible": False
}]

with open('surfaces/surfaces.json', 'w+') as surfaces_json:
    surfaces_json.write(json.dumps(surfaces))
