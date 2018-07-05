#!/usr/bin/env python

import nibabel as nib
import os
import json
import loader

with open('config.json') as config_json:
    config = json.load(config_json)

v1_path = os.path.join(config['freesurfer'], "label/lh.V1.label")
v1 = loader.load_labels(v1_path)

print(v1)