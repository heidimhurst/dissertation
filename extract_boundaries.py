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

from subprocess import check_output
import json, os, argparse

def parse_coords(image_path):
    """
    Correctly formats coordinates list for use in gml string, including
    ensuring that it is closed (e.g. first coordinate is the same as last coordinate)

    Args:
        coord_list: a nested list containing coordinates in the form [[lat,lon],[lat,lon]]
                    must have four entries

    Output:
        returns formmated string
    """

    # determine version of gdal
    gdal_version = check_output(['gdalinfo','--version'])

    # if 2.0 or higher, parse json
    if " 2." in gdal_version:
        # get gdal data
        tiff_info = json.loads(check_output(["gdalinfo","-json", image_path]))
        coord_list = tiff_info['wgs84Extent']['coordinates'][0]

    # if under 2.0, no json to parse
    elif " 1." in gdal_version:
        # get gdal data as big gross string and turn into list of floats
        tiff_info = check_output(['gdalinfo '+image_path], shell=True)
    
        # get coordinate section
        tiff_info = tiff_info[:tiff_info.index('Center')]
        
        coord_list = []
        # get first coordinate set, then cut string
        for location in ["Upper Left", "Lower Left", "Upper Right", "Lower Right"]:
            info = tiff_info[tiff_info.index(location):]
            info = info[info.index('(')+1:info.index(')')]
            # split coordinates and make floats
            coord = [float(x) for x in info.split(",")]
            coord_list.append(coord)

    # swap third and fourth entries to enumerate in reasonable order
    coord_list[3], coord_list[4] = coord_list[4], coord_list[3]

    # parse list of cords to string
    out_coords = ""
    for coords in coord_list:
        out_coords += str(coords[0]) + "," + str(coords[1]) + " "
    out_coords += str(coord_list[0][0]) + "," + str(coord_list[0][1])

    return out_coords


def create_gml(data_location='', outfilename='photo_bounds'):
    """
    Creates a gml file for datavisualization, etc.
    """

    gml_head = '<?xml version="1.0" encoding="utf-8" ?><ogr:FeatureCollection xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="" xmlns:ogr="http://ogr.maptools.org/" xmlns:gml="http://www.opengis.net/gml">'
    gml_foot = "</ogr:FeatureCollection>"

    # initialize counter
    i = 0
    gml_middle = ""
    for filename in os.listdir(data_location):
        if filename.endswith(".tif"):
            # get just file name
            image_name = os.path.splitext(filename)[0]
            
            # add field info
            gml_middle += " <gml:featureMember> <ogr:" + outfilename + " fid=" + '"' + outfilename + '.' + str(i) + '/">'
            gml_middle += '<ogr:geometryProperty> <gml:Polygon srsName="EPSG:4326"> <gml:outerBoundaryIs> <gml:LinearRing> <gml:coordinates>'
            
            # add coordinate info
            gml_middle += parse_coords(os.path.join(data_location,filename))
            
            # close polygon
            gml_middle += "</gml:coordinates> </gml:LinearRing> </gml:outerBoundaryIs> </gml:Polygon> </ogr:geometryProperty> "
            
            # add ID field
            gml_middle += "<ogr:id>" + str(i) + "</ogr:id>"
            
            # add name field equal to original tif name and close tag
            gml_middle += "<ogr:name> " + image_name +" </ogr:name>"
            
            # add close tag
            gml_middle += "</ogr:" + outfilename + "> </gml:featureMember>"

    return gml_head + gml_middle + gml_foot

def write_gml(gml_string, outfiledirectory='.', outfilename="photo_bounds"):
    # write GML string to a file
    out_gml_path = os.path.join(outfiledirectory, outfilename+'.gml')
    with open(out_gml_path, "w") as f:
        f.write(gml_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to images directory")
    parser.add_argument("-o","--output_location",default="",help="Filepath of desired output directory")
    parser.add_argument("-n","--output_name",default="photo_bounds",help="Name of gml file to create, no extension")
    args = parser.parse_args()

    try:
        output_location = args.output_location
    except NameError:
        output_location = input

    gml = create_gml(data_location=args.input, outfilename=args.output_name)
    write_gml(gml, outfiledirectory=output_location, outfilename=args.output_name)


