# import the necessary packages
import mahotas as mh
 
class ImageAdvantage:
	def __init__(self, imagePath):
		# Store the integer image array 
		# used when computing
		# Read an image into a ndarray from a file.
		self.imgArray = mh.imread(imagePath, False)
 
	def croppBoundingBox(self):
		# Returns a version of img cropped to the image’s bounding box.
		# http://mahotas.readthedocs.io/en/latest/api.html#mahotas.croptobbox
		return mh.croptobbox(self.imgArray, 0)

	def centerOfMass(self):
		# Returns the center of mass of img.
		# http://mahotas.readthedocs.io/en/latest/api.html#mahotas.center_of_mass
		# mahotas.center_of_mass(img, labels=None)
		# If labels is given, then it returns L centers of mass, 
		# one for each region identified by labels (including region 0).
		# Return: The exact shape of the output 
		# depends on whether the labels argument was used. 
		# If labels is None, then the return value 
		# is a 1-ndarray of coordinates (size = len(img.shape)); 
		# otherwise, the return value is a 2-ndarray of coordinates 
		# (shape = (labels.max()+1, len(img.shape)).
		return mh.center_of_mass(self.imgArray)

	def skeletonisation(self):
		#Skeletonisation by thinning
		return mh.thin(self.imgArray)

	#mahotas.features.eccentricity(bwimage)
