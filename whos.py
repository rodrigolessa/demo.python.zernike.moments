# Import the necessary packages
from zernike_moments import ZernikeMoments
from searcher import Searcher
import image_utils as iutils
import numpy as np
import argparse
import pickle as cp
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-", "--index", required = True, help = "Path to where the index file will be stored")
ap.add_argument("-q", "--object", required = True, help = "Path to the object image")
args = vars(ap.parse_args())
 
# Load the index
index = open(args["index"], 'rb')
index = cp.load(index)

# Debugging:
print('105Marowak:')
print(index['105Marowak'])

#oad the query image, convert it to grayscale, 
# and resize it
image = cv2.imread(args["object"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = iutils.resize(image, width = 64)

# Threshold the image
thresh = cv2.adaptiveThreshold(image, 255, 
    cv2.ADAPTIVE_THRESH_MEAN_C,
	cv2.THRESH_BINARY_INV, 11, 7)
 
# Initialize the outline image, find the outermost
# contours (the outline) of the object, 
# then draw it
outline = np.zeros(image.shape, dtype = "uint8")
image2, cnts, hierarchy = cv2.findContours(thresh.copy(), 
    cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
# Return the largest area
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
# Fill contours
cv2.drawContours(outline, [cnts], -1, 255, -1)

# Compute Zernike moments to characterize the shape of
# pokemon outline
desc = ZernikeMoments(21)
queryFeatures = desc.describe(outline)
 
# Perform the search to identify the pokemon
searcher = Searcher(index)
# Return 10 first similarities
results = searcher.search(queryFeatures)[:10]

for r in results:
    print(r)

print("That object is: {}".format(results[0][1].upper()))
 
# Show our images
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()