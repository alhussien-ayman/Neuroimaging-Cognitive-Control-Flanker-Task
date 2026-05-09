#!/bin/bash

# Make sure you are inside the folder containing:
# filtered_func_data.nii and MNI152_T1_2mm.nii.gz

# List of voxel coordinates [X Y Z]
# Clusters 6, 5, 4, 3, 2, 1 in order
coords=("33 30 60" "66 19 33" "19 29 34" "23 65 47" "43 71 59" "29 74 33")
indices=(6 5 4 3 2 1)

for i in ${!coords[@]}; do
    c=(${coords[$i]})
    idx=${indices[$i]}

    echo "Processing Cluster $idx at Voxel: ${c[0]} ${c[1]} ${c[2]} ..."

    # 1. Create ROI point
    fslmaths MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi ${c[0]} 1 ${c[1]} 1 ${c[2]} 1 0 1 temp_point_$idx.nii.gz -odt float

    # 2. Convert it into a sphere with 5 mm radius
    fslmaths temp_point_$idx.nii.gz -kernel sphere 5 -fmean temp_sphere_$idx.nii.gz -odt float

    # 3. Convert to binary mask
    fslmaths temp_sphere_$idx.nii.gz -bin Cluster${idx}_Mask.nii.gz

    # 4. Extract mean values from functional data
    fslmeants -i filtered_func_data.nii -m Cluster${idx}_Mask.nii.gz -o Cluster${idx}_values.txt

    # Cleanup temporary files
    rm temp_point_$idx.nii.gz temp_sphere_$idx.nii.gz

    echo "Finished Cluster $idx. File saved as Cluster${idx}_values.txt"
done

echo "All 6 files are ready!"