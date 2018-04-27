# Indexing the dataset by quantifying each image in terms of shape
# Apply the shape descriptor defined to every sprite in dataset. 

# Import the necessary packages
from zernike_moments import ZernikeMoments
#import tkinter
#tkinter._test()
# Just for debugging purposes
from PIL import Image
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

logo = Image("spritesRedBlue\\001Bulbasaur.png")
logo.show()
logo.save("my-image.png")

 
imageFolder = 'spritesRedBlue'
imageFolder = 'spritesRedBlueOLD'
imageExtension = '.png'
imageFinder = '{}/*{}'.format(imageFolder, imageExtension)
imageMoments = 'index.moments'
index = {}

# Initialize descriptor with a radius of 21 pixels, 
# used to characterize the shape of object
zm = ZernikeMoments(21)

#Time to quantify our Pokemon sprites:

# Loop over the sprite images
for spritePath in glob.glob(imageFinder):
	# Parse out the pokemon name, then load the image and
	# \\ usamos dupla a barra de endereço do windows pois é um caracter especial
	# / barra de endereços no Linux
	imageName = spritePath[spritePath.rfind('\\') + 1:].replace(imageExtension, '')
	# convert it to grayscale
	image = cv2.imread(spritePath)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
	# pad the image with extra white pixels to ensure the
	# edges of the pokemon are not up against the borders
	# of the image
	image = cv2.copyMakeBorder(image, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value = 255)
 
	# Invert the image and threshold it
	thresh = cv2.bitwise_not(image)
	thresh[thresh > 0] = 255

	#imf = open('{}_out.png'.format(imageName), 'wb')
	#imf.write(image)

	#debugging

	#img = Image.open(thresh)
	#img.show() 

	#First, we need a blank image to store our outlines — we appropriately a variable called outline on Line 44 and fill it with zeros with the same width and height as our sprite image.

	# Initialize the outline image, find the outermost
	# contours (the outline) of the pokemone, then draw it
	outline = np.zeros(image.shape, dtype = "uint8")

	img2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	contours = sorted(contours, key = cv2.contourArea, reverse = True)[0]

	cv2.drawContours(outline, contours, -1, 255, -1)

	# Compute Zernike moments to characterize the shape of object outline
	moments = zm.describe(outline)

	# Analyse descriptions of form
	print('{}: {}'.format(imageName, moments))

	#retval = cv2.waitKey()

	# then update the index
	index[imageName] = moments


# cPickle for writing the index to file
f = open(imageMoments, "wb")
f.write(cp.dumps(index))
f.close()