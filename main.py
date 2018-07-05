#!/usr/bin/env python

import nibabel as nib
import os
import json
import loader

with open('config.json') as config_json:
    config = json.load(config_json)

v1_path = os.path.join(config['freesurfer'], "label/lh.V1.label")
v1 = loader.load_labels(v1_path)

lh_pial_path = os.path.join(config['freesurfer'], "surf/lh.pial.vtk")
lh_pial = loader.load_vtk(lh_pial_path)

rh_pial_path = os.path.join(config['freesurfer'], "surf/rh.pial.vtk")
rh_pial = loader.load_vtk(rh_pial_path)

num_points = len(lh_pial)
print(num_points)
for i in range(min(50, num_points)):
    print(lh_pial[i], rh_pial[i])