# Indexing the dataset by quantifying each image in terms of shape
# Apply the shape descriptor defined to every sprite in dataset. 

# Import the necessary packages
from zernike_moments import ZernikeMoments
#import tkinter
#tkinter._test()
# Just for debugging purposes
from PIL import Image as pim
#logo = pim.open('spritesRedBlue\\001Bulbasaur.png')
#logo.show()
#print('Image format: {}'.format(logo.format))
#print('Image size: {}'.format(logo.size))
#print('Image mode: {}'.format(logo.mode))
##logo.thumbnail(logo.size)
##logo.save('my-image.png')
import numpy as np
import cv2
#import argparse
import _pickle as cp
import glob
#import pylab as plt
#plt.plot([1,2,3])
#plt.show()
 
# Construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-s", "--sprites", required = True,
#	help = "Path where the sprites will be stored")
#ap.add_argument("-i", "--index", required = True,
#	help = "Path to where the index file will be stored")
#args = vars(ap.parse_args())
 
imageFolder = 'spritesRedBlue'
imageExtension = '.png'
imageFinder = '{}/*{}'.format(imageFolder, imageExtension)
imageMoments = 'index.moments'
imageDebug = 'Abra' #Bulbasaur'
index = {}

# Initialize descriptor with a radius of 21 pixels, 
# used to characterize the shape of object
zm = ZernikeMoments(21)

# Time to quantify sprites:

# Loop over the sprite images
for spritePath in glob.glob(imageFinder):
	# Parse out the image name, then load the image and
	# \\ using double address bar on Windows
	# / address bar on Linux
	imageName = spritePath[spritePath.rfind('\\') + 1:].replace(imageExtension, '')
	
	# Reading the image
	image = cv2.imread(spritePath)

	# Debugging: show original image
	if imageName.find(imageDebug) >= 0:
		cv2.imshow('original', image)
		cv2.waitKey(0)

	# Convert it to grayscale
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Debugging: converted
	if imageName.find(imageDebug) >= 0:
		cv2.imshow('gray', image)
		cv2.waitKey(0)
 
	# pad the image with extra white pixels to ensure the
	# edges of the object are not up against the borders
	# of the image
	image = cv2.copyMakeBorder(image, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value = 255)

	# Debugging: pads along the 4 directions
	if imageName.find(imageDebug) >= 0:
		cv2.imshow('pad', image)
		cv2.waitKey(0)
 
	# Invert the image and threshold it
	thresh = cv2.bitwise_not(image)

	# Debugging: Invert image and threshold it
	if imageName.find(imageDebug) >= 0:
		cv2.imshow('inverted', thresh)
		cv2.waitKey(0)

	thresh[thresh > 0] = 255

	# Debugging: Invert image and threshold it
	if imageName.find(imageDebug) >= 0:
		cv2.imshow('threshold', thresh)
		cv2.waitKey(0)

	#First, we need a blank image to store our outlines — we appropriately a variable called outline on Line 44 and fill it with zeros with the same width and height as our sprite image.

	# Initialize the outline image, find the outermost
	# contours (the outline) of the object, then draw it
	# (fill it with zeros with the same width and height as sprite image)
	outline = np.zeros(image.shape, dtype = "uint8")

	img2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	contours = sorted(contours, key = cv2.contourArea, reverse = True)[0]

	# Draw the contour on outline image
	cv2.drawContours(outline, [contours], -1, 255, -1)

	# Debugging: just outline of the object
	if imageName.find(imageDebug) >= 0:
		cv2.imshow('outline', outline)
		cv2.imwrite('outline.png', outline)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	# Compute Zernike moments to characterize the shape of object outline
	moments = zm.describe(outline)

	# Debugging: analyse descriptions of form
	if imageName.find(imageDebug) >= 0:
		print('{}: {}'.format(imageName, moments))

	# then update the index
	index[imageName] = moments


# cPickle for writing the index to file
f = open(imageMoments, "wb")
f.write(cp.dumps(index))
f.close()