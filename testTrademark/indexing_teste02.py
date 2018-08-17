# Indexing the dataset by quantifying each image in terms of shape.
# Apply the shape descriptor defined to every sprite in dataset.
# Frist we need the outline (or mask) of the object in the image 
# prior to applying Zernike moments. 
# In order to find the outline, we need to apply segmentation

# Import the necessary packages
from zernike_moments import ZernikeMoments
from PIL import Image as pim
import numpy as np
import argparse
import cv2
import pickle as cp
import glob
# Managing windows files
import os
import sys

def _centroid_radius(contourx):
	moment = cv2.moments(contourx)
	cx = int(moment['m10']/moment['m00'])
	cy = int(moment['m01']/moment['m00'])

	ext = []
	ext.append(tuple(contourx[contourx[:, :, 0].argmin()][0])) #left
	ext.append(tuple(contourx[contourx[:, :, 0].argmax()][0])) #Right
	ext.append(tuple(contourx[contourx[:, :, 1].argmin()][0])) #Top
	ext.append(tuple(contourx[contourx[:, :, 1].argmax()][0])) #Bottom
	r = -1
	for e in ext:
		x = np.sqrt((cx-e[0])**2 + (cy-e[1])**2)
		r = x if x>r else r

	return (cx, cy, r)

def _center_radius(contourx):
	center, radius = cv2.minEnclosingCircle(contourx)
	return (center[0], center[1], radius)

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required = True, help = "Path to where the files has stored")

args = vars(ap.parse_args())

imageFolder = "logos_comparacao_ruim\\" + args["folder"]
imageExtension = ".png"
imageFinder = "{}/*{}".format(imageFolder, imageExtension)

index = {}

# Initialize descriptor with a radius of 180 pixels
zm = ZernikeMoments(180)

# Loop over the sprite images
for spritePath in glob.glob(imageFinder):

	# Extract image name, this will serve as unqiue key into the index dictionary.
	# Parse out the image name,
	# \\ using double address bar on Windows
	imageName = spritePath[spritePath.rfind('\\') + 1:].replace(imageExtension, '')

	# Try to manipulate the image if it is possible
	try:
		# then load the image.
		image = cv2.imread(spritePath)

		# Debugging: show original image
		cv2.imshow('original', image)
		cv2.waitKey(0)

		# Convert it to grayscale
		grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# Debugging: converted
		cv2.imshow('grayscale', grayscale)
		cv2.waitKey(0)

		# Apply a blur filter to reduce noise
		blur = cv2.medianBlur(grayscale, 5)

		cv2.imshow('blur', blur)
		cv2.waitKey(0)

		# Bilateral Filter can reduce unwanted noise very well 
		# while keeping edges fairly sharp. 
		# However, it is very slow compared to most filters
		# Filter size: Large filters (d > 5) are very slow, 
		# so it is recommended to use d=5 for real-time applications, 
		# and perhaps d=9 for offline applications that need heavy noise filtering
		blur = cv2.bilateralFilter(blur, 9, 75, 75)

		cv2.imshow('bilateralFilter', blur)
		cv2.waitKey(0)
	
		# THRESH_BINARY = fundo preto or THRESH_BINARY_INV = fundo branco
		_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

		cv2.imshow('thresholded', thresh)
		cv2.waitKey(0)

		centroid_radius = _centroid_radius(contour)

		center_radius = _center_radius(contour)

		cv2.circle(image, (int(centroid_radius[0]),int(centroid_radius[1])), \
             int(centroid_radius[2]), (0,0,255))
		cv2.circle(image, (int(centroid_radius[0]),int(centroid_radius[1])), \
             2, (0, 0, 255), -1)

		cv2.circle(image, (int(center_radius[0]), int(center_radius[1])), \
             int(center_radius[2]), (0,255,0))
		cv2.circle(image, (int(center_radius[0]), int(center_radius[1])), \
             2, (0,255,0), -1)

        cv2.imshow("Mask Complete", img)
        cv2.waitKey(0)

		# Compute Zernike moments to characterize the shape of object outline
		moments = zm.describe(thresh)

		print("Image moments:")
		print(moments.shape)
		print('{}: {}'.format(imageName, moments))

		cv2.destroyAllWindows()

	except:
		pass