#!/bin/bash

# loop over desired training sets
# declare -a sf=("3")

# initialize required variables
trial=t7
object_type=car
prefix=car #or cars or whatever

base_path=/home/uceshhu

project_path=${base_path}/runs/t7_ssd_inception
data_path=${base_path}/xview_data
personal_util_path=${base_path}/personal_codebase/dissertation
xview_util_path=${base_path}/xview_codebase/data_utilities
model_name=/ssd_inception

models_research_path=${base_path}/tf_api_codebase/models/research

# scale factors of interest
# declare -a sf=("1.5" "2.5" "3" "3.5")
declare -a sf=("1.5" "2.5" "3")

# loop through each of these and train/eval
for i in ${sf[@]}; do
	# setup variables
	factor=$i
	config_name=${prefix}_${trial}_${factor}.config
	config_path=${project_path}/models${model_name}/${config_name}
	project_data_path=${project_path}/data/${object_type}/${factor}

	screen_name=${trial}_eval_${factor}
	
	# initialize screen
	screen -L -d -m  -S ${screen_name}

	# create eval command 
	eval_command="cd ${models_research_path} && export PYTHONPATH=$PYTHONPATH:${models_research_path}:${models_research_path}/slim && CUDA_VISIBLE_DEVICES='2' python object_detection/eval.py \
	--logtostderr \
	--pipeline_config_path=${config_path} \
	--checkpoint_dir=${project_path}/models${model_name}/${object_type}/${factor}/train \
	--eval_dir=${project_path}/models${model_name}/${object_type}/${factor}/eval"

	# start evaluation in a different screen
	screen -S $screen_name -X stuff "${eval_command}"$(echo -ne '\015')

	# move to requisite folder
	cd ${models_research_path}
	export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

	# run a train job IN THIS SCREEN
	CUDA_VISIBLE_DEVICES='0,1' python object_detection/train.py --num_clones=2 --logtostderr \
	--pipeline_config_path=${config_path} \
	--train_dir=${project_path}/models${model_name}/${object_type}/${factor}/train

	# kills screen of eval command, killing eval command
	screen -S ${screen_name} -X quit
done
