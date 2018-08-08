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
ap.add_argument("-i", "--index", required = True, help = "Path to where the index file will be stored")
ap.add_argument("-o", "--object", required = True, help = "The object name")

args = vars(ap.parse_args())
 
# Load the index
index = open(args["index"], 'rb')
index = cp.load(index)

# Debugging:
#print(index[args["object"]])

queryFeatures = index[args["object"]]

# Perform the search to identify the image
searcher = Searcher(index)
# Return x first similarities
results = searcher.search(queryFeatures)[:20]

for r in results:
    #imageZeros = '{-:0>3}'.format(imageNumber)
    if r[0] < 0.14:
        print("Similar: {} - {}".format(r[1].upper(), r[0]))
        image = cv2.imread("logos/{}.png".format(r[1]))
        cv2.imshow('outline', image)
        cv2.waitKey(0)
    else:
        print("nop: {} - {}".format(r[1].upper(), r[0]))

cv2.destroyAllWindows()