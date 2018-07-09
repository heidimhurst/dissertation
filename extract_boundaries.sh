#!/bin/bash

# first argument should be path to folder to evaluate

# output file variable location (default to current directory if not set)
OUTLOCATION="${2:-.}"
echo "$OUTLOCATION"

LINESEP=" , "

# for all tiff files in folder
shopt -s nullglob
for i in /$1/*.tif; do
	gdalinfo -json $i >> $OUTLOCATION
	echo $(basename $i)
done

