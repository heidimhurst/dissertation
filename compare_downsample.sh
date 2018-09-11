#!/bin/bash

base_path=/Users/heidihurst/Documents/UK/ucl-gis/dissertation
data_path=${base_path}/data
personal_util_path=${base_path}/dissertation
source_dir=104
target_dir=downsample

# loop through each downsampling method  downsample image  rename appropriately

declare -a methods=('near' 'bilinear' 'cubic' 'cubicspline' 'lanczos' 'average' 'mode')
declare -a factors=(1)

cd ${data_path}/${target_dir}

for i in ${factors[@]}; do
	for j in ${methods[@]}; do
		# downsample by factor of...
		python ${personal_util_path}/downsample.py \
		-i ${data_path}/${source_dir} \
		-o ${data_path}/${target_dir} \
		-r $j -s $i

		mv 104.tif 104_${j}_${i}.tif
	done
done
