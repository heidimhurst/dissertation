#!/bin/bash

# setup definitions
trial=t7
object_type=car
prefix=car #or cars or whatever

base_path=/home/uceshhu

project_path=${base_path}/runs/t7_ssd_inception
data_path=${base_path}/xview_data
personal_util_path=${base_path}/personal_codebase/dissertation
xview_util_path=${base_path}/xview_codebase/baseline/inference
model_name=/ssd_inception

models_research_path=${base_path}/tf_api_codebase/models/research

declare -a factors=(1.5 2 2.5 3 3.5)

cd ${models_research_path}
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

cd ${xview_util_path}

# i=1
# loop through all factors of interest
for i in ${factors[@]}; do
	echo ------------------- $i ------------------- 
	# set directory location of saved model, test images, etc
	# path to froxen_model.pb
	saved_model_path=${project_path}/models${model_name}/${object_type}/${i}/saved_model_*/frozen_inference_graph.pb
	# path to images
	test_image_path=${data_path}/test_images_${i}
	# folder to save .txt. files to
	output_folder=${project_path}/models${model_name}/${object_type}/${i}/test_detections

	# make folder if it doesn't exist
	mkdir $output_folder

	echo $saved_model_path
	echo $output_folder

	cd ${test_image_path}
	# loop through filenames
	for filename in *.tif; do
		echo 'FILENAME: '$filename
		bname=$(basename $filename)
		echo 'BASENAME: '$bname
		output_path=${output_folder}/${bname%.*}.tif.txt
		echo 'OUTPUT PATH: '$output_path
		# run inference
		CUDA_VISIBLE_DEVICES='-1' python ${xview_util_path}/create_detections.py -c ${saved_model_path} -o ${output_path} ${filename}

	done
done
