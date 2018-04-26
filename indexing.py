# Indexing the dataset
# Apply the shape descriptor defined to every sprite in dataset. 

# Import the necessary packages
from zernike_moments import ZernikeMoments
import numpy as np
import argparse
import _pickle as cp
import glob
import cv2
 
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
imagePickle = 'index.cpickle'

# initialize our descriptor (Zernike Moments with a radius
# of 21 used to characterize the shape of our pokemon) and
# our index dictionary
desc = ZernikeMoments(21)
index = {}

#Time to quantify our Pokemon sprites:

# loop over the sprite images
#for spritePath in glob.glob(args["sprites"] + "/*.png"):
for spritePath in glob.glob(imageFinder):
	# parse out the pokemon name, then load the image and
	# convert it to grayscale
	pokemon = spritePath[spritePath.rfind("/") + 1:].replace(imageExtension, "")
	image = cv2.imread(spritePath)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
	# pad the image with extra white pixels to ensure the
	# edges of the pokemon are not up against the borders
	# of the image
	image = cv2.copyMakeBorder(image, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value = 255)
 
	# invert the image and threshold it
	thresh = cv2.bitwise_not(image)
	thresh[thresh > 0] = 255

	#First, we need a blank image to store our outlines — we appropriately a variable called outline on Line 44 and fill it with zeros with the same width and height as our sprite image.

	# initialize the outline image, find the outermost
	# contours (the outline) of the pokemone, then draw
	# it
	outline = np.zeros(image.shape, dtype = "uint8")

	img2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	contours = sorted(contours, key = cv2.contourArea, reverse = True)[0]

	cv2.drawContours(outline, contours, -1, 255, -1)

	# compute Zernike moments to characterize the shape
	# of pokemon outline, then update the index
	moments = desc.describe(outline)
	index[pokemon] = moments


# write the index to file
#f = open(args["index"], "w")
f = open(imagePickle, "wb")
f.write(cp.dumps(index))
f.close()