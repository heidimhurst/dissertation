#!/bin/bash

# using score .py

base_path="/home/uceshhu"

project_path='${base_path}/runs/t7_ssd_inception"
data_path=${base_path}/xview_data
personal_util_path=${base_path}/personal_codebase/dissertation
xview_util_path=${base_path}/xview_codebase/baseline/scoring
model_name=/ssd_inception

models_research_path=${base_path}/tf_api_codebase/models/research


python score.py /pfs/$input_repo/ $groundtruth --output /pfs/out/$timestamp