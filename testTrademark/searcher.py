# Comparing Shape Descriptors

# Import the necessary packages
from scipy.spatial import distance as dist
 
class Searcher:
	def __init__(self, index):
		# store the index that we will be searching over
		self.index = index
 
	def search(self, queryFeatures):
		# initialize our dictionary of results
		results = {}
 
		# loop over the images in our index
		for (k, features) in self.index.items():
			# Compute the distance between the query features
			# and features in our index, then update the results
			d = dist.euclidean(queryFeatures, features)
			#print('Distance: {}'.format(d))
			results[k] = d
 
		# Sort our results, where a smaller distance indicates
		# higher similarity
		results = sorted([(v, k) for (k, v) in results.items()])
 
		# return the results
		return results