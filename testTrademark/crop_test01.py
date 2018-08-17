# Import the necessary packages
import image_utils as iutils
import numpy as np
import pickle as cp
import argparse
import cv2
import sys

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--object", required = True, help = "The object name that we want to crop")

args = vars(ap.parse_args())

# load image
img = cv2.imread(args["object"])
#rsz_img = cv2.resize(img, None, fx=0.25, fy=0.25) # resize since image is huge
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale

blur = cv2.medianBlur(gray, 5)

blur2 = cv2.bilateralFilter(blur, 9, 75, 75)

# threshold to get just the signature
retval, thresh_gray = cv2.threshold(blur2, thresh=100, maxval=255, type=cv2.THRESH_BINARY)

# find where the signature is and make a cropped region
points = np.argwhere(thresh_gray==0) # find where the black pixels are
points = np.fliplr(points) # store them in x,y coordinates instead of row,col indices
x, y, w, h = cv2.boundingRect(points) # create a rectangle around those points
#x, y, w, h = x-10, y-10, w+20, h+20 # make the box a little bigger
x, y, w, h = x, y, w+5, h+5 # make the box a little bigger

#crop = blur2[y:y+h, x:x+w] # create a cropped region of the gray image

crop = img[y:y+h, x:x+w]
cv2.imshow("Crop the original", crop)

# get the thresholded crop
#retval, thresh_crop = cv2.threshold(crop, thresh=200, maxval=255, type=cv2.THRESH_BINARY)

# display
#cv2.imshow("Cropped and thresholded image", thresh_crop) 
#cv2.waitKey(0)
cv2.destroyAllWindows()