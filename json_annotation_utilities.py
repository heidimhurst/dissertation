# Original work 2018 copyright HMHurst, heidimhurst.github.io
# Available under Apache 2.0 License

import json
import math
import argparse
from tqdm import tqdm

'''
Helper functions to read in xView dataset geojson label file and 
process appropriately, including extracting just one type of object
and downsampling the bounding boxes for objects.
'''

def clean_types(input_dict):
    """
    Sets all type_ids to 1, for simplicity.  Do not use with multiple type IDs!

    Args:
        input_dict: dictionary of geojson content in xView schema

    Output:
        returns dictionary
    """

    for item in input_dict['features']:
        item['properties']['type_id'] = 1

    return input_dict

def parsetype_dict(input_dict, type_id=[18]):
    """
    Extracts features with specific type ids from dictionary.

    Args:
        input_dict: dictionary of geojson content in xView schema
        type_id: list of integers of categories of interest (see https://github.com/DIUx-xView/baseline/blob/master/xview_class_labels.txt)

    Output:
        returns dictionary 
    """

    # Filter python objects with list comprehensions
    input_dict['features'] = [x for x in input_dict['features'] if x['properties']['type_id'] in type_id]

    return input_dict

def parsetype(input_json="../data/xView_train.geojson", 
              output_file='output_json_test.geojson', 
              type_id=[18]):
    """
    Extracts entries in xview_train geojson corresponding to given type id and resaves
    as new geojson.

    Args:
        input_json: filepath to original xView training geojson
        output_file: filepath (including extension) to desired output geojson file
        type_id: list of integers of categories of interest 
                 (see https://github.com/DIUx-xView/baseline/blob/master/xview_class_labels.txt)

    Output:
        saves new .geojson file to disk
    """

    # read input file
    with open(input_json) as f:
        output_dict = json.load(f)

    # Filter python objects with list comprehensions
    output_dict = parsetype_dict(output_dict, type_id)

    # Transform python object back into json
    output_json = json.dumps(output_dict)

    # write output_json to file for future use
    with open(output_file, 'w') as outfile:  
        json.dump(output_dict, outfile)


def downsample_bbox_dict(input_dict, scale_factor=2.0):
    """
    Performs downsampling functionality for geojson format.  

    Args:
        input_dict: dictionary of geojson in xView structure (must contain coordinates
                    in input_dict['features'][i]['properties']['bounds_imcoords'])
        scale_factor: amount that the image is reduced by in EACH DIRECTION. 
                      e.g. scale factor of 2 reduces the overall image size by 1/4

    Output:
        Returns same dictionary with coordinates divided by scale_factor in each direction.
    """

    # need to modify bounds_imcoords for all features
    for i in tqdm(range(len(input_dict['features']))):
        # get coordinate string & parse (format is xmin,ymin,xmax,ymax)
        coords = [int(x) for x in input_dict['features'][i]['properties']['bounds_imcoords'].split(',')]

        # divide all coords by scale factor, taking floor of mins and ceil of maxes
        out_coords = str(int(math.floor(coords[0]/scale_factor))) + "," + \
                str(int(math.floor(coords[1]/scale_factor))) + "," + \
                str(int(math.ceil(coords[2]/scale_factor))) + "," + \
                str(int(math.ceil(coords[3]/scale_factor)))

        # modify dictionary
        input_dict['features'][i]['properties']['bounds_imcoords'] = out_coords
    
    return input_dict


def downsample_bbox(input_json="../data/xView_train.geojson", 
                      output_file='output_json_test.geojson', 
                      scale_factor=2.0):
    """
    Downsamples the bounding boxes present in training geojson file to match downsampled image. 
    Saves as new geojson.

    Args:
        input_json: filepath to original xView training geojson
        output_file: filepath (including extension) to desired output geojson file
        scale_factor: amount that the image is reduced by in EACH DIRECTION. 
                      e.g. scale factor of 2 reduces the image size by 1/4

    Output: 
        saves new .geojson file to disk
    """

    # read input file
    with open(input_json) as f:
        output_dict = json.load(f)

    # perform downsampling
    output_dict = downsample_bbox_dict(output_dict, scale_factor)

    # Transform python object back into json
    output_json = json.dumps(output_dict)

    # write output_json to file for future use
    with open(output_file, 'w') as outfile:  
        json.dump(output_dict, outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to original json")
    parser.add_argument("-s", "--scale_factor", type=float, help="Factor by which JSON should be reduced in each direction")
    parser.add_argument("-o","--output", default="modified_bounds.geojson", help="Filepath of desired output")
    parser.add_argument("-t","--type_id", nargs='+', type=int, help="List of type ids to be selected")
    parser.add_argument("-c","--clean_types", action='store_true', help="Set all type ids to 1")
    
    args = parser.parse_args()

    # read input file
    with open(args.input) as f:
        output_dict = json.load(f)

    # filter if required
    if args.type_id:
        output_dict = parsetype_dict(output_dict, args.type_id)

    # set all type values to 1 if required
    if args.clean_types:
        print "WARNING: Removing all type ids, setting type to 1"
        output_dict = clean_types(output_dict)

    # downsample if required
    if args.scale_factor:
        output_dict = downsample_bbox_dict(output_dict, float(args.scale_factor))

    # export
    if args.output:
        # Transform python object back into json
        output_json = json.dumps(output_dict)

        # write output_json to file for future use
        with open(args.output, 'w') as outfile:  
            json.dump(output_dict, outfile)


    
