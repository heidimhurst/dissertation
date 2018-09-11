"""
Heidi M Hurst heidimhurst.github.io
Apache License 2018

"""

import numpy as np
import json, argparse, logging, os

from pandas import DataFrame as df
import pandas as pd

"""
Utilities to get statistics for each downsampled bounding box.
Stats of interest: average area, average height, average width.
Designate whether in train/val or test split.
"""

test_set = ['1042.tif','1085.tif','1193.tif','1430.tif','1457.tif','1604.tif',
            '724.tif','887.tif','1044.tif','1104.tif','129.tif','1436.tif',
            '1463.tif','601.tif','742.tif','89.tif','1053.tif','111.tif',
            '136.tif','1446.tif','1466.tif','606.tif','791.tif','924.tif',
            '1076.tif','1132.tif','1399.tif','144.tif','1565.tif','684.tif',
            '819.tif','1084.tif','1178.tif','1420.tif','1450.tif','1593.tif',
            '692.tif','886.tif']

def get_dimensions(im_coords):
    """
    Given a string of image coordinates, extracts the height and
    width of an an image.

    Args:
        im_coords: string containing four comma separated image 
        coordiante numbers

    Returns:
        height: height (y direction) in pixels
        width: width (x direction) in pixels
    """
    coords = [int(x) for x in im_coords.split(',')]

    width = (coords[2]-coords[0])
    height = (coords[3]-coords[1])

    return height, width


def is_test(feature, test_set):
    """
    Returns boolean true if the feature was in a test set image.

    Args:
        feature: full bounding box feature
        test_set: list of image names that were used for test set

    Returns:
        bool: true if bbox was in test set
    """

    # extract just the name and return bool 
    return feature['properties']['image_id'] in test_set


def process_json(filepath, test_set=test_set):
    """
    Function to read in a geojson of bounding boxes and export two
    CSV files: stats for each bbox and overall stats.

    Args:
        filepath: path to JSON file
        test_set: list of images used for testing

    Returns:
        numpy (n x 4) array of height, width, area is_test bool

    """
    
    # read in JSON file
    with open(filepath) as f:
        raw_data = json.load(f)
        logging.info("Data read in from {}".format(filepath))

    # create dummy numpy array (4 x n boxes)
    processed_data = np.zeros((len(raw_data['features']),4))

    # for each feature, record length, height, area, and test set boolean
    for i in range(len(raw_data['features'])):
        # extract coordinates
        im_coords = raw_data['features'][i]['properties']['bounds_imcoords']
        # convert coordinates to height, width
        height, width = get_dimensions(im_coords)
        # add fields to processed_data for later
        processed_data[i,:] = [height, width, height*width, \
                               is_test( raw_data['features'][i], test_set)]

    return processed_data



def save_single_summary_stats(processed_data, out_path="bbox_processing"):
    """
    Computes summary statistics of interest for later use.

    Statistics computed:
        for height, width, area: min, max, mode, median, std
        for bool: number

    Args:
        processed_data: np array countaining nx4 entries (height, width, area, bool)
        output_path: location to save stats csv file

    Returns:
        saves stats to csv file

    """
    # compute statistics using pandas
    pd_df = df(processed_data)
    pd_summary = df.describe()
    # save to csv file
    pd_summary.to_csv(out_path + "_summary.csv")



def process_and_save(json_path, test_set=test_set, out_path="bbox_processing"):
    """
    Process a single json file and save result to CSV

    Args:
        json_path: path to geojson file of interest 
        test_set: list of images used for testing
        out_path: location to save csv

    Returns:
        none, saves CSV
    """
    # process results 
    processed_data = process_json(json_path)
    # write out to csv
    np.savetxt(out_path + ".csv" , processed_data, delimiter=',')
    # log
    # logging.INFO("File {} written to {}".format(json_path, out_path))


def process_folder(parent_folder, test_set= test_set, out_path="bbox_processing", 
                   save_each=False, save_summary=True):
    """
    Looks through all subfolders of provided json folder and saves information from any
    geojson found to a CSV file

    Args:
        parent_folder: folder to search, including all subfolders
        test_set: list of images used for testing
        out_path: location to save csv as PREFIX (without .csv)
        save_each: boolean to save each file information as separate csv
        save_summary: boolean to export total summary info to csv

    Returns:
        none, saves CSVs
    """

    # get all relevant files
    jsonfiles = [os.path.join(root, name)
             for root, dirs, files in os.walk(parent_folder)
             for name in files
             if name.endswith(".geojson")]

    # create dummy for saving combined summary information
    if save_summary:
        all_df = []

    # loop through and process
    for j_file in jsonfiles:
        # extract name, for outpath
        f_name = os.path.basename(j_file)
        f_name = f_name[0:f_name.rfind(".geojson")]

        if save_each:
            # name for each file
            name = out_path + "_" + f_name + ".csv"
            # save each one off separately if desired
            process_and_save(json_path=j_file, test_set=test_set, out_path=name)
	    logging.info("Full information for {} saved to {}".format(j_file, name))
        # if we just want summary statistics
        if save_summary:
            # get summary statistics df
            f_df = df(process_json(j_file, test_set))
            f_df.columns = ["height", "width", "area", "test"]
            f_summary = f_df.describe()
            # name for outfile
            all_df.append(f_summary)

    # save out combined summary statistics
    if save_summary:
        # extract just file names for naming
        # file_names = [os.path.basename(f) for f in jsonfiles]
        file_names = [f[f.rfind("/")+1:f.rfind(".geojson")] for f in jsonfiles]
        # concatenate mega df
        all_summary = pd.concat(all_df, keys=file_names)
        # save off
        all_summary.to_csv(out_path + "_summary.csv")
	logging.info("Summary saved to {}_summary.csv".format(out_path))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Path to folder or geojson file of interest")
    parser.add_argument("-e", "--save_each", action="store_true", \
                        help="Store exported information from each geojson as separate csv")
    parser.add_argument("-s", "--save_summary", action="store_true", \
                        help="Store summary information for all files as one csv")
    parser.add_argument("out_path", help="Location & prefix to store csv files.  LEAVE OFF csv ending.")

    args = parser.parse_args()

    # logging utility
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger(__name__)

    # processing for if the file path is a geojson file
    if os.path.isfile(args.filepath) and args.filepath.endswith(".geojson"):
        logging.info("Processing output for geojson")

        processed_data = process_json(args.filepath)
        # if save summary
        if args.save_summary:
            save_single_summary_stats(processed_data, args.out_path)
            logging.info("Single summary statistic csv saved to {}_summary.csv".format(args.out_path))
        # if save single 
        if args.save_each:
            np.savetxt(out_path + ".csv" , processed_data, delimiter=',')
            logging.info("Info for single file {} saved to {}.csv".format(args.filepath, args.out_path))

    # processing for if the filepath is a folder
    elif os.path.isdir(args.filepath):
        logging.info("Processing {} and its subfolders... this may take some time.".format(args.filepath))
        # process all
        process_folder(parent_folder=args.filepath, test_set=test_set, out_path=args.out_path,
                       save_each=args.save_each, save_summary=args.save_summary)

    # catchall
    else:
        logging.WARNING("Input filepath ({}) neither geojson nor directory.  Please try again.".format(args.filepath))



