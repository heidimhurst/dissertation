trial=t9
object_type=car
prefix=car #or cars or whatever

base_path=/home/uceshhu

project_path=${base_path}/runs/${trial}_ssd_inception
data_path=${base_path}/xview_data
personal_util_path=${base_path}/personal_codebase/dissertation
xview_util_path=${base_path}/xview_codebase/data_utilities
model_name=/ssd_inception

models_research_path=${base_path}/tf_api_codebase/models/research

declare -a factors=(1 1.5 2 2.5 3 3.5 4)
declare -a step_val=(31607 37346 30016 48939 28203 33959 37662)

cd ${models_research_path}
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

for i in {0..6}; do
	factor=${factors[i]}
	config_name=${prefix}_${trial}_${factor}.config
	config_path=${project_path}/models${model_name}/${config_name}

	step=${step_val[i]}

	trained_checkpoint_prefix=${project_path}/models${model_name}/${object_type}/${factor}/train/model.ckpt-${step}
	export_dir=${project_path}/models${model_name}/${object_type}/${factor}/saved_model_${step}


	INPUT_TYPE=image_tensor

	echo $config_path
	echo $trained_checkpoint_prefix
	echo $export_dir
	CUDA_VISIBLE_DEVICES='-1' python object_detection/export_inference_graph.py \
	     --input_type=${INPUT_TYPE} \
	     --pipeline_config_path=${config_path} \
	     --trained_checkpoint_prefix=${trained_checkpoint_prefix} \
	     --output_directory=${export_dir}
done
