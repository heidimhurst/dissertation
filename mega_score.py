# script to run inference for like everything

# import scoring functionality
from score import score

# TODO: turn this into function

factors = ["1", "1.5", "2", "2.5", "3", "3.5", "4"]

base_path="/home/uceshhu"
trial="t7"
object_type="car"
prefix="car"

project_path="{}/runs/t7_ssd_inception".format(base_path)
data_path="{}/xview_data".format(base_path)
personal_util_path="{}/personal_codebase/dissertation".format(base_path)
xview_util_path="{}/xview_codebase/baseline/scoring".format(base_path)
model_name="/ssd_inception"

models_research_path="{}/tf_api_codebase/models/research".format(base_path)
output_csv="{}/models{}/{}/{}_{}_performance.csv".format(project_path, model_name, object_type, prefix, trial)

# factor =

# create for loop for each downsample factor
results=np.zeroes([7*19, 6])
for i in tqdm(range(length(factors))):
	factor=factors[i]

	# ----- project specific definitions
	project_data_path="{}/data/{}/{}".format(project_path, object_type, factor)
	# run python script to process json 
	groundtruth="{}/{}_{}_{}.geojson".format(project_data_path, prefix, trial, factor)

	saved_model_path="{}/models{}/{}/{}/saved_model_*/frozen_inference_graph.pb".format(project_path, model_name, object_type, factor)
	# path to images
	test_image_path="{}/test_images_{}".format(data_path, factor)
	# folder to save .txt. files to
	detection_folder="{}/models{}/{}/{}/test_detections/".format(project_path, model_name, object_type, factor)
	output_folder="{}/models{}/{}/{}/test_evaluation".format(project_path, model_name, object_type, factor)

	# create for loop for each desired IOU 
	for j in range(5,100,5):
		iou_threshold=j/100.0
		print "Calculating performance for downsample factor {} at IOU {}".format(factor, iou_threshold)
		# run processing
		result=score(detection_folder, groundtruth, 'test.txt', iou_threshold=iou_threshold)
		# append result to numpy array
		results[i*19 + ((j/5)-1),]=[float(factor),iou_threshold,result['map'],result['map_score'], result['mar_score'], result['f1']]

# save results to specified CSV
np.savetxt(output_csv, results, delimiter=',')
