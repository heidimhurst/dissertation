#!/bin/bash

# using score .py

base_path=/home/uceshhu

project_path=${base_path}/runs/t7_ssd_inception
data_path=${base_path}/xview_data
personal_util_path=${base_path}/personal_codebase/dissertation
xview_util_path=${base_path}/xview_codebase/baseline/scoring
model_name=/ssd_inception

models_research_path=${base_path}/tf_api_codebase/models/research

# set factor
i=4
factor=$i

project_data_path=${project_path}/data/${object_type}/${factor}
# run python script to process json 
groundtruth=${project_data_path}/${prefix}_${trial}_${factor}.geojson 

saved_model_path=${project_path}/models${model_name}/${object_type}/${i}/saved_model_*/frozen_inference_graph.pb
# path to images
test_image_path=${data_path}/test_images_${i}
# folder to save .txt. files to
detection_folder=${project_path}/models${model_name}/${object_type}/${i}/test_detections
output_folder=${project_path}/models${model_name}/${object_type}/${i}/test_evaluation


mkdir -p $output_folder

python score.py $detection_folder/ $groundtruth --output $output_folder