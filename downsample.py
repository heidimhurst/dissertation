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

from subprocess import check_output,call
from tqdm import tqdm
import json, os, argparse, math

def check_resample_method(string):
    """
    Ensures that selected resample method is available to GDAL.  Use for argument validation
    """
    resample_methods = ['near','bilinear','cubic','cubicspline','lanczos','average','mode']
    if string not in resample_methods:
        raise argparse.ArgumentTypeError("Resampling method must be one of ".join([str(x) for x in resample_methods]))

    return string

def get_imsize(image_path):
    """
    Gets the x dimension of an image.  Varies based on version of GDAL available.

    Args:
        image path: path to single image of interest

    Returns:
        size: int, in pixels of the x direction size of the image
    """

    # determine version
    gdal_version = check_output(['gdalinfo','--version'])

    # if 2.0 or higher
    if " 2." in gdal_version:
        size = json.loads(check_output(["gdalinfo","-json", image_path]))['size'][0]
    # if under 2.0
    elif " 1." in gdal_version:
        # get result as string
        command = 'gdalinfo ' + image_path + ' | grep "Size is"'
        size_string = check_output([command], shell=True)
        # cut after comma
        size_string = size_string[:size_string.index(',')]
        # cut to last 
        size_string = size_string[size_string.rfind(" ")+1:]

        size = int(size_string)

    return size

def downsample_image(image_path, downsample_factor=2.0, resample_method='lanczos', 
                     output_location=os.path.join(os.getcwd(),'downsampled')):
    """
    Downsamples an image using GDALWARP utility.

    Args:
        image path: path to single image
        downsample_factor: amount by which to reduce the size of the image in each direction
        resample method: method (must be available to GDAL)
        output_location: place to put newly downsampled images - creates a new downsampled 
                         folder if there isn't one already to prevent overwriting

    """

    # get image size from gdalinfo
    size = get_imsize(image_path)
    size = math.ceil(size/float(downsample_factor))
    # call gdalwarp to create new image
    image_name = os.path.basename(image_path)
    call(["gdalwarp -ts " + str(size) + " 0 -r " + resample_method + " " + image_path + " " + os.path.join(output_location, image_name)], shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",default=os.getcwd(), help="Path to images directory")
    parser.add_argument("-o","--output_location",default=os.path.join(os.getcwd(),"downsampled"),help="Filepath of desired output directory")
    parser.add_argument("-r","--resample_method",default="near",type=check_resample_method, help="GDAL approved resampling method (see current gdal version for more info)")
    parser.add_argument("-s","--scale_factor",default=2.0,type=float, help="Downsample scale factor (values > 1 will SHRINK image)")
    parser.add_argument("-u","--upsample",action="store_true", help="If flag -u is used, inverts scale factor (values > 1 will GROW image)")
    args = parser.parse_args()

    # create output directory, if it doesn't yet exist
    try:
        output_location = args.output_location
        print "Output specified - saving to " + output_location
    except NameError:
        output_location = os.path.join(os.getcwd(),"downsampled")
        print "No output specified - saving to " + output_location
    if not os.path.isdir(output_location):
        os.makedirs(output_location)
        print "Saving to " + args.output_location

    # specify what scale factor is used
    if args.upsample:
        scale_factor = 1.0/args.scale_factor
        print "Upsampling - scale factor set to {}".format(scale_factor)
    else:
        scale_factor = args.scale_factor
        print "Downsampling - scale factor set to {}".format(scale_factor)

    # look through all files and downsample
    for file in os.listdir(args.input):
        if file.endswith(".tif"):
            downsample_image(os.path.join(args.input, file), scale_factor, 
                             args.resample_method, args.output_location)
            print "Downsampled image "+file

