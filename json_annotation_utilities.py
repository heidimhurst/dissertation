# Original work 2018 copyright HMHurst, heidimhurst.github.io
# Available under Apache 2.0 License

import json
import math

'''
Helper functions to read in xView dataset geojson label file and 
process appropriately, including extracting just one type of object
and downsampling the bounding boxes for objects.
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

	# read input file
	with open(input_json) as f:
	    output_dict = json.load(f)

	# Filter python objects with list comprehensions
	output_dict['features'] = [x for x in output_dict['features'] if x['properties']['type_id'] == type_id]

	# Transform python object back into json
	output_json = json.dumps(output_dict)

	# write output_json to file for future use
	with open(output_file, 'w') as outfile:  
	    json.dump(output_dict, outfile)


def downsample_bbox(input_json="../data/xView_train.geojson", 
			  		output_file='output_json_test.geojson', 
			  		scale_factor=2):
	"""
	Downsamples the bounding boxes present in training geojson file to match downsampled image. 
	Saves as new geojson.

	Args:
		input_json: filepath to original xView training geojson
		output_file: filepath (including extension) to desired output geojson file
		scale_factor: amount that the image is reduced by in EACH DIRECTION. 
					  e.g. scale factor of 2 reduces the image size by 1/4

	Oputput: 
		saves new .geojson file to disk

	"""

	# read input file
	with open(input_json) as f:
	    output_dict = json.load(f)

	# need to modify bounds_imcoords for all features
	for i in range(len(output_dict['features'])):
	    # get coordinate string & parse (format is xmin,ymin,xmax,ymax)
	    coords = [int(x) for x in output_dict['features'][i]['properties']['bounds_imcoords'].split(',')]

	    # divide all coords by scale factor, taking floor of mins and ceil of maxes
	    out_coords = str(math.floor(coords[0]/scale_factor)) + "," + \
	            str(math.floor(coords[1]/scale_factor)) + "," + \
	            str(math.ceil(coords[2]/scale_factor)) + "," + \
	            str(math.ceil(coords[3]/scale_factor))

        # modify dictionary
	    output_dict['features'][i]['properties']['bounds_imcoords'] = out_coords

    	# Transform python object back into json
	output_json = json.dumps(output_dict)

	# write output_json to file for future use
	with open(output_file, 'w') as outfile:  
	    json.dump(output_dict, outfile)




