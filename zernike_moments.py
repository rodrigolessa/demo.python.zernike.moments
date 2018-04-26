# import the necessary packages
import mahotas as mh
 
class ZernikeMoments:
	def __init__(self, radius):
		# store the size of the radius that will be
		# used when computing moments
		self.radius = radius
 
	def describe(self, image):
		# return the Zernike moments for the image
		return mh.features.zernike_moments(image, self.radius)