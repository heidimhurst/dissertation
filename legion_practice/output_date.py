# python script to write a random number of timestamps to a file

from datetime import datetime
import random

with open('out.txt', 'w') as outfile:
    for i in range(random.randint(5, 10)):
        outfile.write(str(datetime.now()))
        outfile.write('\n')

