#!/usr/bin/env python

import nibabel as nib
import os
import json
import loader
import nibabel as nib
import numpy as np

with open('config.json') as config_json:
    config = json.load(config_json)

r2 = nib.load('input/prf/r2.fixed.nii');
print(r2.get_sform())


lh_pial = loader.load_vtk(os.path.join(config['freesurfer'], "surf/lh.pial.vtk"))
rh_pial = loader.load_vtk(os.path.join(config['freesurfer'], "surf/rh.pial.vtk"))
lh_inflated = loader.load_vtk(os.path.join(config['freesurfer'], "surf/lh.inflated.vtk"))
rh_inflated = loader.load_vtk(os.path.join(config['freesurfer'], "surf/rh.inflated.vtk"))
lh_white = loader.load_vtk(os.path.join(config['freesurfer'], "surf/lh.white.vtk"))
rh_white = loader.load_vtk(os.path.join(config['freesurfer'], "surf/rh.white.vtk"))

output = []

for i in range(len(lh_pial)):
    entry = {
        'pial': {
            'left': lh_pial[i],
            'right': rh_pial[i]
        },
        'white': {
            'left': lh_white[i],
            'right': rh_white[i]
        },
        'inflated': {
            'left': lh_inflated[i],
            'right': rh_inflated[i]
        }
    }
    
    output.append(entry)

with open('output.json', 'w+') as output_json:
    output_json.write(json.dumps(output))