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

args = vars(ap.parse_args())

imageFolder = args["folder"] #'logos'
imageExtension = '.' + args["extension"].lower() #'.png'
imageFinder = '{}/*{}'.format(imageFolder, imageExtension)
imageFolderContrast = 'logo_'

# If index file exists, try to delete
try:
    os.remove(imageFolderContrast)
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
zm = ZernikeMoments(180)

imagesInFolder = glob.glob(imageFinder)

qt = len(imagesInFolder)

i = 1

# Loop over the sprite images
for spritePath in imagesInFolder:

	# Extract image name, this will serve as unqiue key into the index dictionary.
	imageName = spritePath[spritePath.rfind('\\') + 1:].lower().replace(imageExtension, '')

	# Try to manipulate the image if it is possible
	try:
		progress(i, qt)

		# then load the image.
		image = cv2.imread(spritePath)

		# Convert it to grayscale
		grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# Bilateral Filter can reduce unwanted noise very well
		blur = cv2.bilateralFilter(grayscale, 9, 75, 75)

		# Then, any pixel with a value greater than zero (black) is set to 255 (white)
		_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

		# Compute Zernike moments to characterize the shape of object outline
		moments = zm.describe(thresh)

		# then update the index
		index[imageName] = moments

		i+=1

	except:
		pass

# cPickle for writing the index in a file
with open(imageMomentsFile, "wb") as outputFile:
	cp.dump(index, outputFile, protocol=cp.HIGHEST_PROTOCOL)