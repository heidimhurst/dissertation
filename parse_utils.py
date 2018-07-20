"""
Copyright 2018 Heidi M Hurst github.io/heidimhurst
All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
"""

from subprocess import call
import csv, argparse

def parse_file(info_file):
    """
    Parses an info file created by the chipping utility to create a txt file
    with all the information we want in it yay.

    Args:
        info_file: path to file containing outputs from process_wv.py
    Returns:
        test: int number of test chips
        train: int number of training chips
        chips: int total number of chips
        boxes: int total number of objects
    """

    with open(info_file, 'r') as info:
        # read in as a string
        data = info.read().replace('\n', '')
        # find substring containing chip information
        test = int(data[data.rfind(':') + 1:data.rfind('test')].strip())
        # cut off last info section of data
        data = data[:data.rfind('INFO')]
        # find substring iwth training information
        train = int(data[data.rfind(':') + 1:data.rfind('train')].strip())
        # total number of chips
        chips = int(data[data.find("Chips:")+6:data.rfind("INFO")].strip())
        # cut off last info section of data
        data = data[:data.rfind('INFO')]
        # total number of boxes
        boxes = int(data[data.find("Tot Box:")+8:data.rfind("INFO")].strip())

    return test, train, chips, boxes


def modify_config(config_path, test):
    """
    Modifies a specified config file with the correct number of test chips.

    Args:
        config_path: path to configuration file
        test: integer number of test chips
    
    Returns:
        no return
    """

    call(['sed -i "s+{NUM}+'+str(test)+'+g" '+config_path], shell=True)

def write_results(factor=-1, results=(-1,-1,-1,-1), out_file='tfrecord_info.csv'):
    """
    Writes statistics from info file to end of outfile.

    Args:
        results: integer touple (test, train, chips, boxes) from parse_file (-1 as default)
        out_file: path to csv file where info should be written

    Returns:
        none
    """
    # write processed results to formatted csv file in order factor test train chips boxes
    with open(out_file, 'a') as o:
            writer = csv.writer(o, delimiter=',')
            writer.writerow([factor] + list(results))


def process_info_file(info_file, factor=-1, out_file=None, config_path=None):
    """
    Reads in info file, processes to csv outfile, and modifies requisite config path.

    Args:
        info_file: path to file containing outputs from process_wv.py
        out_file: path to csv file where info should be written
        config_path: path to configuration file to be modified

    Returns:
        no returns.
    """

    # extract information from info file
    results = parse_file(info_file)

    # write results to outfile, if desired
    if out_file:
        write_results(factor, results, out_file)

    # process config file, if desired
    if config_path:
        modify_config(config_path, results[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to output file containing information")
    parser.add_argument("-o","--output_csv", help="Desired csv output, with location")
    parser.add_argument("-c","--config_path", help="Path to configuration file to change")
    parser.add_argument("-f", "--factor", type=float, help="Downsample factor")
    args = parser.parse_args()

    process_info_file(args.input, args.factor, args.output_csv, args.config_path)
