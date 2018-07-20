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
# declare -a sf=("1.5" "2.5" "3" "3.5")
declare -a sf=("3")

# loop through each of these
for i in ${sf[@]}; do
	factor=$i
	config_name=${prefix}_${trial}_${factor}.config
	config_path=${project_path}/models${model_name}/${config_name}
	project_data_path=${project_path}/data/${object_type}/${factor}
	# let user know what's up
	echo ----------- Creating images for downsample factor $i -----------
	# create folder for downsampled images
	mkdir ${data_path}/train_images_${factor}
	# downsample images
	python ${personal_util_path}/downsample.py \
	-i ${data_path}/train_images \
	-o ${data_path}/train_images_${factor} \
	-r lanczos -s ${factor}
	# create file structure
	echo ----------- Creating required folders for object $object_type at factor $i -----------
	interim_path=${project_path}/models${model_name}/${object_type}/${factor}
	mkdir ${interim_path}
	mkdir ${interim_path}/eval ${interim_path}/train
	mkdir $project_data_path
	# create JSON file
	echo ----------- Creating JSON file for downsample factor $i -----------
	python ${personal_util_path}/json_annotation_utilities.py \
	${data_path}/xView_train.geojson \
	-c -t ${id} -s ${factor} \
	-o ${project_path}/data/${object_type}/${factor}/${prefix}_${trial}_${factor}.geojson
	# create appropriate config files, modify as needed
	echo ----------- Creating project config file ${config_path} -----------
	cp ${project_path}/models${model_name}/t7_template.config ${config_path}
	# replace train path
	sed -i "s+{TFR_TRAIN}+\"${project_path}/data/${object_type}/${factor}/xview_train_${trial}_${factor}.record\"+g" ${config_path}
	# # replace evaluation path
	sed -i "s+{TFR_EVAL}+\"${project_path}/data/${object_type}/${factor}/xview_test_${trial}_${factor}.record\"+g" ${config_path}
	# # replace label map path
	sed -i "s+{LABEL}+\"${project_path}/data/${object_type}/map_${trial}.pbtxt\"+g" ${config_path}
	# # replace model checkpoint
	sed -i "s+{CHECKPOINT}+\"${project_path}/models${model_name}/model.ckpt\"+g" ${config_path}
	# create tfrecord files
	echo ----------- Creating tfrecord files for factor $i ----------- 
	# pipe output to a file for processing
	# make sure you're in teh correct directory
	cd ${project_data_path}
	# create tfrecord file and pipe input to save for later processing
	python ${xview_util_path}/process_wv.py -t .1 -s ${trial}_${factor} \
	${data_path}/train_images_${factor}/ \
	${project_data_path}/${prefix}_${trial}_${factor}.geojson 2>&1 | tee ${project_data_path}/processing_output.txt
	# process information from tf record file 
	echo ----------- Processing TF Record Output Info -----------
	# run parse utilities
	python ${personal_util_path}/parse_utils.py \
	${project_data_path}/processing_output.txt \
	-o ${project_path}/data/${object_type}/${object_type}_processing.csv \
	-f ${factor} -c ${config_path}
	
done