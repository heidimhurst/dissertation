#!/bin/bash

# project variables
trial=t7
# factor=1.5

id=18 #89 #18: small car; 89: shipping container lot
object_type=car
prefix=car #or cars or whatever

base_path=/home/uceshhu

project_path=${base_path}/runs/t7_ssd_inception
data_path=${base_path}/xview_data
personal_util_path=${base_path}/personal_codebase/dissertation
xview_util_path=${base_path}/xview_codebase/data_utilities
model_name=/ssd_inception


# scale factors of interest
declare -a sf=("1.5" "2.5" "3" "3.5")

# loop through each of these
for i in ${sf[@]}; do
	factor=$i
	# let user know what's up
	echo ----------- Creating images for downsample factor $i -----------
	# create folder for downsampled images
	mkdir ${data_path}/train_images_${factor}
	# downsample images
	python ${personal_util_path}/downsample.py \
	-i ${data_path}/train_images \
	-o ${data_path}/train_images${factor} \
	-r lanczos -s ${factor}
	# create file structure
	echo ----------- Creating required folders for object $object_type at factor $i -----------
	interim_path=${project_path}/models${model_name}/${object_type}/${factor}
	mkdir ${interim_path}/eval ${interim_path}/train
	mkdir ${project_path}/data/${object_type}/${factor}
	# create JSON file
	echo ----------- Creating JSON file for downsample factor $i -----------
	python ${personal_util_path}/json_annotation_utilities.py \
	${data_path}/xView_train.geojson \
	-c -t ${id} -s ${factor} \
	-o ${project_path}/data/${object_type}/${factor}/${prefix}_${trial}_${factor}.geojson
	# create tfrecord files
	echo ----------- Creating tfrecord files for factor $i ----------- 
	cd ${project_path}/data/${object_type}/${factor}
	python ${xview_util_path}/process_wv.py -t .1 -s ${trial}_${factor} \
	${data_path}/train_images_${factor}/ \
	${project_path}/data/${object_type}/${factor}/${prefix}_${trial}_${factor}.geojson
	# create appropriate 
	
done