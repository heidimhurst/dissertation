#!/bin/bash

# import for all factors
declare -a factors=(1 1.5 2 2.5 3 3.5 4)
declare -a trials=(t7 t9)

# import for a specific image as specified
pic=${1:-89}


for t in ${trials[@]}; do
	for i in ${factors[@]}; do
		scp uceshhu@deeplearning.cege.ucl.ac.uk:/home/uceshhu/runs/${t}_ssd_inception/models/ssd_inception/car/${i}/test_detections/${pic}.tif.txt ${t}_${i}_${pic}.tif.txt
	done
done
