#!/bin/bash
dir_freesurfer=$(jq -r ".freesurfer" config.json)
dir_prf=$(jq -r ".prf" config.json)

echo "Converting files..."

mkdir output
cd output

mris_convert "$dir_freesurfer/surf/lh.pial lh.pial.vtk"
mris_convert "$dir_freesurfer/surf/lh.white lh.white.vtk"
mris_convert "$dir_freesurfer/surf/lh.inflated lh.inflated.vtk"

mris_convert "$dir_freesurfer/surf/rh.pial rh.pial.vtk"
mris_convert "$dir_freesurfer/surf/rh.white rh.white.vtk"
mris_convert "$dir_freesurfer/surf/rh.inflated rh.inflated.vtk"

cd ..

cp "$dir_prf/r2.nii" output/

./main.py

gzip output/r2.nii