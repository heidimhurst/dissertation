base_path=/home/uceshhu

data_path=${base_path}/xview_data
personal_util_path=${base_path}/personal_codebase/dissertation

# source_dir=test_images


declare -a factors=(1 1.5 2 2.5 3 3.5 4)

for i in ${factors[@]}; do
	source_dir=test_images_${i}
	target_dir=test_images_upsample_${i}
	mkdir ${data_path}/${target_dir}

	# downsample by factor of...
	python ${personal_util_path}/downsample.py \
	-i ${data_path}/${source_dir} \
	-o ${data_path}/${target_dir} \
	-u -r lanczos -s $i
done


