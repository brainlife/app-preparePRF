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

import nibabel as nib
import os
import json
import loader
import nibabel as nib
import numpy as np

print("Successfully imported everything")

with open('config.json') as config_json:
    config = json.load(config_json)

# loading r2
r2 = nib.load('output/r2.nii')
r2_data = r2.get_fdata()
xform = np.mat(r2.get_sform())
inv_xform = np.linalg.inv(xform)

output = {}#{ 'surfaces': surfaces, 'color_maps': color_maps, 'morph_maps': morph_maps }

with open('output.json', 'w+') as output_json:
    output_json.write(json.dumps(output))