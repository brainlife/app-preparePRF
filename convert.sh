#!/bin/bash
dir_freesurfer=$(jq -r ".freesurfer" config.json)
dir_prf=$(jq -r ".prf" config.json)

echo "Converting files..."

mris_convert "$dir_freesurfer/surf/lh.pial" "surfaces/lh.pial.vtk"
mris_convert "$dir_freesurfer/surf/lh.white" "surfaces/lh.white.vtk"
mris_convert "$dir_freesurfer/surf/lh.inflated" "surfaces/lh.inflated.vtk"

mris_convert "$dir_freesurfer/surf/rh.pial" "surfaces/rh.pial.vtk"
mris_convert "$dir_freesurfer/surf/rh.white" "surfaces/rh.white.vtk"
mris_convert "$dir_freesurfer/surf/rh.inflated" "surfaces/rh.inflated.vtk"
