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

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required = True, help = "Path to where the files has stored")
ap.add_argument("-e", "--extension", required = True, help = "Extension of the images")
ap.add_argument("-i", "--index", required = True, help = "Path to where the index file will be stored")
ap.add_argument("-d", "--debug", required = False, help = "The object name for debugging")

args = vars(ap.parse_args())

imageFolder = args["folder"] #'logos'
imageExtension = '.' + args["extension"] #'.png'
imageFinder = '{}/*{}'.format(imageFolder, imageExtension)
imageMomentsFile = args["index"] #'index.pkl'
imageDebug = args["debug"]
debugPath = 'logos_debug'
index = {}

# If index file exists, try to delete
try:
    os.remove(imageMomentsFile)
except OSError:
    pass

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 

# Initialize descriptor with a radius of 160 pixels 
# (is the maximum size of the images), 
# used to characterize the shape of object
zm = ZernikeMoments(180)

imagesInFolder = glob.glob(imageFinder)

qt = len(imagesInFolder)

i = 0

# Loop over the sprite images
for spritePath in imagesInFolder:
	
	i+=1

	progress(i, qt)

	# Extract image name, this will serve as unqiue key into the index dictionary.
	# Parse out the image name,
	# \\ using double address bar on Windows
	# / address bar on Linux
	imageName = spritePath[spritePath.rfind('\\') + 1:].replace(imageExtension, '')

	# Try to manipulate the image if it is possible
	try:
		# then load the image.
		image = cv2.imread(spritePath)
		# TODO: Migrate to Image class
		#self.original = cv2.imread(path)

		# Debugging: show original image
		if imageName.find(imageDebug) >= 0:
			cv2.imshow('original', image)
			cv2.waitKey(0)

		# HACK: Not necessary
		# Pad the image with extra white pixels to ensure the
		# edges of the object are not up against the borders
		# of the image
		image = cv2.copyMakeBorder(image, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value = 255)

		# Debugging: pads along the 4 directions
		if imageName.find(imageDebug) >= 0:
			cv2.imshow('pad', image)
			cv2.waitKey(0)


		# Convert it to grayscale
		grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# TODO: Migrate to a function in Image class
		#self.grayscale = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)		

		# Debugging: converted
		if imageName.find(imageDebug) >= 0:
			cv2.imshow('grayscale', grayscale)
			cv2.waitKey(0)

		# Apply a blur filter to reduce noise
		blur = cv2.medianBlur(grayscale, 5)

		if imageName.find(imageDebug) >= 0:
			cv2.imshow('blur', blur)
			cv2.waitKey(0)

		# Bilateral Filter can reduce unwanted noise very well 
		# while keeping edges fairly sharp. 
		# However, it is very slow compared to most filters
		# Filter size: Large filters (d > 5) are very slow, 
		# so it is recommended to use d=5 for real-time applications, 
		# and perhaps d=9 for offline applications that need heavy noise filtering
		blur = cv2.bilateralFilter(blur, 9, 75, 75)

		cv2.imwrite(os.path.join(debugPath , '{}_blur.png'.format(imageName)), blur)

		if imageName.find(imageDebug) >= 0:
			cv2.imshow('bilateralFilter', blur)
			cv2.waitKey(0)
	
		# For segmentation: Flip the values of the pixels 
		# (black pixels are turned to white, and white pixels to black).
		# NOTE: Replaced by BilateralFilter
		#thresh = cv2.bitwise_not(image)

		# Debugging: Invert image
		#if imageName.find(imageDebug) >= 0:
			#cv2.imshow('inverted', thresh)
			#cv2.waitKey(0)

		# Then, any pixel with a value greater than zero (black) is set to 255 (white)
		# NOTE: First version
		#thresh[thresh > 0] = 255
		# NOTE: Second version
		# THRESH_BINARY = fundo preto or THRESH_BINARY_INV = fundo branco
		_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

		# Debugging: Invert image and threshold it
		if imageName.find(imageDebug) >= 0:
			cv2.imshow('thresholded', thresh)
			cv2.waitKey(0)

		# TODO: Reinforce contours

		# First, we need a blank image to store outlines
		# we appropriately a variable called outline 
		# and fill it with zeros with the same width and height as the sprite image.

		# Accessing Image Properties
		# Image properties include number of rows, columns and channels, 
		# type of image data, number of pixels etc.
		# Shape of image is accessed by img.shape. It returns a tuple of number of rows, 
		# columns and channels (if image is color):
		outline = np.zeros(thresh.shape, dtype = "uint8")

		# Initialize the outline image,
		# find the outermost contours (the outline) of the object, 
		# cv2.RETR_EXTERNAL - telling OpenCV to find only the outermost contours.
		# cv2.CHAIN_APPROX_SIMPLE - to compress and approximate the contours to save memory
		img2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# Sort the contours based on their area, in descending order. 
		# keep only the largest contour and discard the others.
		contours = sorted(contours, key = cv2.contourArea, reverse = True)[0]

		# The outline is drawn as a filled in mask with white pixels:
		cv2.drawContours(outline, [contours], -1, 255, -1)

		cv2.imwrite(os.path.join(debugPath , '{}_outline.png'.format(imageName)), outline)

		# Debugging: just outline of the object
		if imageName.find(imageDebug) >= 0:
			cv2.imshow('outline', outline)
			cv2.waitKey(0)

		# TODO: Show center of mass with radius mask

		# Compute Zernike moments to characterize the shape of object outline
		moments = zm.describe(thresh)

		# Debugging: analyse descriptions of form
		if imageName.find(imageDebug) >= 0:
			print("Image moments:")
			print(moments.shape)
			print('{}: {}'.format(imageName, moments))

		# then update the index
		index[imageName] = moments

		cv2.destroyAllWindows()

		# NOTE: Functions MAP(), REDUCE()
		#images = map(pim.open, ['original.png', 'blur.png', 'outline.png'])
		#widths, heights = zip(*(i.size for i in images))

		#total_width = sum(widths)
		#max_height = max(heights)

		#new_im = pim.new('RGB', (total_width, max_height))

		#x_offset = 0
		#for im in images:
			#new_im.paste(im, (x_offset,0))
			#x_offset += im.size[0]

		#new_im.save(os.path.join(debugPath , '{}_outline.png'.format(imageName)))

		# Debugging: just write the original image and the threshold with radius mask
		#cv2.imwrite(os.path.join(debugPath , '{}_outline.png'.format(imageName)), new_img)
	except:
		pass

# cPickle for writing the index in a file
with open(imageMomentsFile, "wb") as outputFile:
	cp.dump(index, outputFile, protocol=cp.HIGHEST_PROTOCOL)