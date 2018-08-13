# Import the necessary packages
from zernike_moments import ZernikeMoments
from searcher import Searcher
import image_utils as iutils
import numpy as np
import argparse
import pickle as cp
import cv2
import sys

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-", "--index", required = True, help = "Path where the index file be stored")

args = vars(ap.parse_args())
 
# Load the index
index = open(args["index"], 'rb')
index = cp.load(index)

# Perform the search to identify the image
searcher = Searcher(index)

#for obj in index:
#RuntimeError: dictionary changed size during iteration

for obj in index:

    # Debugging:
    #print(obj)
    #print(index[obj])

    # Return 30 first similarities
    results = searcher.search(index[obj])[:30]

    for r in results:
        #imageZeros = '{-:0>3}'.format(imageNumber)
        image_to_delete = r[1]
        image_distance = r[0]
        if image_distance <= 0.011:
            print("Similar: {} - {}".format(image_to_delete, image_distance))
            # TODO: Write images name in a table
            # try to delete the given user, handle if the user doesn't exist.
            try:
                del index[image_to_delete]
            except KeyError:
                print("{image} doesn't exist in index".format(image=image_to_delete))
                pass
        elif image_distance <= 0.051:
            print("barely: {} - {}".format(image_to_delete, image_distance))

#cv2.destroyAllWindows()