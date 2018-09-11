#!/bin/bash

declare -a factors=(1 1.5 2 2.5 3 3.5 4)

# if no input used, image pulled will be 104
pic=${1:-104}

# it no input used, image will be pulled from train set
set=${2:-train}

# upsampled
# for i in ${factors[@]}; do
# 	scp uceshhu@deeplearning.cege.ucl.ac.uk:/home/uceshhu/xview_data/${set}_images_upsample_${i}/${pic}.tif ${pic}_upsample_${i}.tif
# done


for i in ${factors[@]}; do
	scp uceshhu@deeplearning.cege.ucl.ac.uk:/home/uceshhu/xview_data/${set}_images_${i}/${pic}.tif ${pic}_downsample_${i}.tif
done