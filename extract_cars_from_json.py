# Original work 2018 copyright HMHurst, heidimhurst.github.io
# Available under Apache 2.0 License

import json

'''
Helper function to read in xView dataset geojson label file and 
extract only objects of interest (e.g. with specific type id).
Writes resultant geojson to new file
'''

def parsetype(input_json="../data/xView_train.geojson", 
			  output_file='output_json_test.geojson', 
			  type_id=18):
	"""
	Extracts entries in xview_train geojson corresponding to given type id and resaves
	as new geojson.

	Args:
		input_json: filepath to original xView training geojson
		output_file: filepath (including extension) to desired output geojson file
		type_id: integer of category of interest (see https://github.com/DIUx-xView/baseline/blob/master/xview_class_labels.txt)

	Output:
		saves new .geojson file to disk

	"""
	#input_json = "../data/xView_train.geojson"
	#output_file = 'output_json_test.geojson'
	#type_id = 18

	# read input file
	with open(input_json) as f:
	    data = json.load(f)

	# copy initial dictionary to preserve categories, structure
	output_dict = data

	# Filter python objects with list comprehensions
	output_dict['features'] = [x for x in data['features'] if x['properties']['type_id'] == type_id]

	# Transform python object back into json
	output_json = json.dumps(output_dict)

	# write output_json to file for future use
	with open(output_file, 'w') as outfile:  
	    json.dump(output_dict, outfile)

