# python script to list images in a given directory

import sys
import os

default_path = '/home/uceshhu/xview_data/train_images'

# if only one argument, look for files there, else use default
if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
    path = sys.argv[1]
else:
    path = default_path

# filter for only image files
images = [x for x in os.listdir(path) if x.endswith('tif')]

# print to console
print(images)

# and write to a file
with open('out.txt', 'w') as outfile:
    for i in images:
        outfile.write(i)
        outfile.write('\n')
