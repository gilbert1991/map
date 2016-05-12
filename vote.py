import numpy as np

import file_handler as fh
import setting as st

def neighborVoting(des_list, img_list, result, dist):
	# Generate a list of lengths of each descriptors
	index = [len(des) for des in des_list] 
	# Accumulate the lengths to identify the image in which the nearest-neighbor locates
	index = [sum(index[:length]) for length in range(1, len(index) + 1)]

	# Initiate the weights of images to zero
	weights = np.zeros(len(img_list))

	# K * (id of nearest neighbor in feature dataset, distance to the neighbor) of a descriptor in query image
	for rslt, dt in zip(result, dist):
		# (id of nearest neighbor in feature dataset, distance to the neighbor) of KNN of the descirptor in query image
		for r, d in zip(rslt, dt):
			# Get the id of image in which the 'r' locates
			pos = np.searchsorted(index, r)

			# Calculate the weight
			weights[pos] = weights[pos] + weightScore(d)
			# print "Observation %d in dataset with distance %f weights %f for location: %s" % (r, d, weight, img_list[pos].geo)			

	# norm to 1
	weights = weights / weights.sum(axis=0)

	# assign the weights to image objects
	for v, img in zip(weights, img_list):
		img.weight = v
		# if v > 0:
		# 	print "%s %d has vote %d" % (img.location.geo, img.cameraPara.heading, v)

	fh.writeList(weights, st.path + "vote.txt")

	maxImage = img_list[weights.argmax(axis=0)]

	return img_list, weights, maxImage

def weightScore(distance):
	# Add a deviation to dist to avoid numerial error
	weight = 1 / (distance + 1e-7)

	return weight

def analysisHeadingWeights(img_list, headings):
	# create len(headings) empty arrays
	weights_headings = [[0 for x in range(0)] for y in range(len(headings))]

	# Sort weights according to headings
	for img in img_list:
		# get the index in headings pol
		index = headings.index(img.cameraPara.heading)
		# add weight to the array of its heading
		weights_headings[index].append(img.weight)

	# list of tuples contains std, mean, lists
	analysis = []

	for idx, head in enumerate(headings):
		info = {'heading': head}

		# add weights list to dict
		# info['weights'] = weights_headings[idx]

		# add population standard deviation to dict
		arr = np.array(weights_headings[idx])
		info['std'] = arr.std()
		info['mean'] = arr.mean()
		info['max'] = arr.max()

		analysis.append(info)

	return analysis


