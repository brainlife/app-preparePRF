#!/bin/bash
dir_freesurfer=$(jq -r ".freesurfer" config.json)
dir_prf=$(jq -r ".prf" config.json)

echo "Converting files..."

mris_convert "$dir_freesurfer/surf/lh.pial" "$dir_freesurfer/surf/lh.pial.vtk"
mris_convert "$dir_freesurfer/surf/lh.white" "$dir_freesurfer/surf/lh.white.vtk"
mris_convert "$dir_freesurfer/surf/lh.inflated" "$dir_freesurfer/surf/lh.inflated.vtk"

mris_convert "$dir_freesurfer/surf/rh.pial" "$dir_freesurfer/surf/rh.pial.vtk"
mris_convert "$dir_freesurfer/surf/rh.white" "$dir_freesurfer/surf/rh.white.vtk"
mris_convert "$dir_freesurfer/surf/rh.inflated" "$dir_freesurfer/surf/rh.inflated.vtk"
