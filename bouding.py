# Import the necessary packages
from image_advantage import ImageAdvantage
# Just for debugging purposes
from PIL import Image as pim
import numpy as np
import cv2
import argparse
import pickle as cp
import glob

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--sprites", 
	required = True,
	help = "Image path to computing")
#ap.add_argument("-i", "--index", required = True,
#	help = "Path to where the index file will be stored")

args = vars(ap.parse_args())
 
# Initialize image functions
iad = ImageAdvantage(args["sprites"])

imgbb = iad.croppBoundingBox()

cv2.imshow('Bounding box', imgbb)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(iad.centerOfMass())

