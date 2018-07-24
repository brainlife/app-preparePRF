#!/usr/bin/env python

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
    
    if weight < 1.0/6.0:
        r = 1.0
        g = weight * 6.0
    elif weight < 2/6:
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
t1 = nib.load(config['t1'])
r2 = nib.load(os.path.join(config['prf'], 'r2.nii.gz'))

t1_data = t1.get_fdata()
r2_data = r2.get_fdata()

volume_width, volume_height, volume_depth = t1_data.shape
t1_qform = t1.get_qform().tolist()

# load everything
print("loading files...")
lh_pial = loader.load_vtk('surfaces/lh.pial.vtk')
rh_pial = loader.load_vtk('surfaces/rh.pial.vtk')

lh_white = loader.load_vtk('surfaces/lh.white.vtk')
rh_white = loader.load_vtk('surfaces/rh.white.vtk')

lh_inflated = loader.load_vtk('surfaces/lh.inflated.vtk')
rh_inflated = loader.load_vtk('surfaces/rh.inflated.vtk')

# get inverse xform 
inv_xform = np.matmul(np.linalg.inv(r2.get_sform()), t1_qform)

lh_surface = {
    "left": True,
    "name": "Left Pial Surface",
    "vcolor": [],
    "filename": "lh.pial.vtk",
    "filetype": "vtk",
    "morphTarget": "lh.inflated.vtk",
    "qform": t1_qform
}
rh_surface = {
    "right": True,
    "name": "Right Pial Surface",
    "vcolor": [],
    "filename": "rh.pial.vtk",
    "filetype": "vtk",
    "morphTarget": "rh.inflated.vtk",
    "qform": t1_qform
}

print("calculating overlay... (left hemisphere)")
for i in range(len(lh_pial)):
    lh_inflated[i][0] -= 60
    
    # perform same adjustment as in Justin's app
    # (translating each vertex by half the volume size)
    lh_pial[i][0] += volume_width / 2
    lh_pial[i][1] += volume_height / 2
    lh_pial[i][2] += volume_depth / 2
    
    lh_inflated[i][0] += volume_width / 2
    lh_inflated[i][1] += volume_height / 2
    lh_inflated[i][2] += volume_depth / 2
    
    x = (lh_pial[i][0] + lh_white[i][0] + volume_width / 2) * .5
    y = (lh_pial[i][1] + lh_white[i][1] + volume_height / 2) * .5
    z = (lh_pial[i][2] + lh_white[i][2] + volume_depth / 2) * .5
    
    r2_coord = np.matmul(inv_xform, np.mat([[x], [y], [z], [1]]))
    coords_flat = [int(x) for x in r2_coord.flatten().tolist()[0]]
    
    color = 0x808080
    if inside_bounds(coords_flat[0], coords_flat[1], coords_flat[2], r2.shape):
        r2_value = r2_data[coords_flat[0], coords_flat[1], coords_flat[2]]
        
        if np.isfinite(r2_value):
            r2_r, r2_g, r2_b = weight2heat(r2_value)
            color = (int(r2_r * 255.0) << 16) + (int(r2_g * 255.0) << 8) + int(r2_b * 255.0)
    
    lh_surface['vcolor'].append(color)

print("calculating overlay... (right hemisphere)")
for i in range(len(rh_pial)):
    rh_inflated[i][0] += 60
    
    rh_pial[i][0] += volume_width / 2
    rh_pial[i][1] += volume_height / 2
    rh_pial[i][2] += volume_depth / 2
    
    rh_inflated[i][0] += volume_width / 2
    rh_inflated[i][1] += volume_height / 2
    rh_inflated[i][2] += volume_depth / 2
    
    x = (rh_pial[i][0] + rh_white[i][0] + volume_width / 2) * .5
    y = (rh_pial[i][1] + rh_white[i][1] + volume_height / 2) * .5
    z = (rh_pial[i][2] + rh_white[i][2] + volume_depth / 2) * .5
    
    r2_coord = np.round(np.matmul(inv_xform, np.mat([[x], [y], [z], [1]])))
    coords_flat = [int(x) for x in r2_coord.flatten().tolist()[0]]
    
    color = 0x808080
    if inside_bounds(coords_flat[0], coords_flat[1], coords_flat[2], r2.shape):
        r2_value = r2_data[coords_flat[0], coords_flat[1], coords_flat[2]]
        
        if np.isfinite(r2_value):
            r2_r, r2_g, r2_b = weight2heat(r2_value)
            color = (int(r2_r * 255.0) << 16) + (int(r2_g * 255.0) << 8) + int(r2_b * 255.0)
    
    rh_surface['vcolor'].append(color)

print("writing everything...")
loader.update_vtk('surfaces/lh.pial.vtk', lh_pial)
loader.update_vtk('surfaces/rh.pial.vtk', rh_pial)

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

print("finished")
