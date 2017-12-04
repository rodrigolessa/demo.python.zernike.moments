# Now that we have our shape descriptor defined, we need to apply it to every Pokemon sprite in our database. This is a fairly straightforward process so I’ll let the code do most of the explaining. Let’s open up our favorite editor, create a file named index.py, and get to work:

# import the necessary packages
from mypy.zernikemoments import ZernikeMoments
import numpy as np
import argparse
import cPickle
import glob
import cv2
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--sprites", required = True,
	help = "Path where the sprites will be stored")
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the index file will be stored")
args = vars(ap.parse_args())
 
# initialize our descriptor (Zernike Moments with a radius
# of 21 used to characterize the shape of our pokemon) and
# our index dictionary
desc = ZernikeMoments(21)
index = {}

#Time to quantify our Pokemon sprites:

# loop over the sprite images
for spritePath in glob.glob(args["sprites"] + "/*.png"):
	# parse out the pokemon name, then load the image and
	# convert it to grayscale
	pokemon = spritePath[spritePath.rfind("/") + 1:].replace(".png", "")
	image = cv2.imread(spritePath)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
	# pad the image with extra white pixels to ensure the
	# edges of the pokemon are not up against the borders
	# of the image
	image = cv2.copyMakeBorder(image, 15, 15, 15, 15,
		cv2.BORDER_CONSTANT, value = 255)
 
	# invert the image and threshold it
	thresh = cv2.bitwise_not(image)
	thresh[thresh > 0] = 255

	#First, we need a blank image to store our outlines — we appropriately a variable called outline on Line 44 and fill it with zeros with the same width and height as our sprite image.

	# initialize the outline image, find the outermost
	# contours (the outline) of the pokemone, then draw
	# it
	outline = np.zeros(image.shape, dtype = "uint8")
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
	cv2.drawContours(outline, [cnts], -1, 255, -1)