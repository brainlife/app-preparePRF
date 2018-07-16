# app-preparePRF

A brain life application to prepare PRF and freesurfer data to be visualized with ui-3dsurfaces

## Preparing Inputs

Run `Freesurfer` on Brain Life with the **non-ACPC Aligned** `s017_canonical.nii` or the T1 image that you are using to conduct pRF analysis. Then run `pRF` (Justin Gardner's app) using your appropriate stimulus (`stim.nii.gz`) and task (`bold.nii.gz`).

Run this app with the respective outputs from Freesurfer and pRF.

## Outputs

The only output from this app is a single `surfaces.json` file containing the appropriate mapping for each surface:

```javascript
[
    {
        "left": true,
        "name": "Left Pial Surface",
        "vcolor": [16842799, 16842799, 16842799/*, ...*/],
        "filename": "lh.pial.vtk",
        "filetype": "vtk",
        "morphTarget": "lh.inflated.vtk"
    },
    {
        "left": true,
        "name": "Left Inflated Surface",
        "vcolor": [16842841, 16842841, 16842841/*, ...*/],
        "filename": "lh.inflated.vtk",
        "filetype": "vtk"
    },
    // ...
]
```

(This app will also write the bold.nii.gz sform to r2.nii)

## How Parsing output from Freesurfer Works

Freesurfer will output a folder called `output/` with a few things in it. Namely, the `surf/` folder contains the list of surfaces and the `label/` folder contains a list of 'lookup table' like files (for all the `.label` files).

The leftmost value in each of the label files corresponds to the index of the associated vertex in each surface. For example, each of the labels given for `lh.V1.label` correspond to both the vertices in `lh.pial` (the original surface) and `lh.inflated` (the inflated surface).

I used `mris_convert` to output `lh.pial` and `lh.inflated` as `lh.pial.vtk` and `lh.inflated.vtk` (though you could parse through the original binary files as well). This gives you a list of vertices and faces, and the index of each vertex corresponds to the leftmost entry in each label file. But importantly, there's now a way to map from any given vertex on the original pial surface to its associated vertex on the inflated one. This means that we can overlay data like `r2.nii` (from pRF) on the inflated surface.