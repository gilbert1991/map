import matplotlib.pyplot as plt
import numpy

import http_handler as hh
import file_handler as fh
import my_util as mt
import objects as obj
import register as rgstr
import feature as ftr

file_path = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/"

def initQuery(location, cameraPara):
	# 1. Initialize the fields of query image 
	query = obj.Image()
	query.location = location # Starting GPS
	query.cameraPara = cameraPara
	query.filePath = file_path + "image/test/test.jpeg"

	# Load query image
	if cameraPara != None:
		encoded_args = hh.encodeStreetArgs(location.geo, cameraPara.size, cameraPara.fov, cameraPara.heading, cameraPara.pitch);
		fh.img2File(hh.getStreetView(encoded_args), query.filePath)

	return query

def neighborVoting(des_list, img_list, result, dist):
	# Create list of #des in each image to indicate the  
	index = [0]
	for des in des_list: 
		index.append(index[-1] + len(des))
	index.pop(0)

	# Voting with the distances
	votes = numpy.zeros(len(img_list))

	for rslt, dt in zip(result, dist):		
		for r, d in zip(rslt, dt):
			pos = numpy.searchsorted(index, r)

			# Add a small value to dist to avoid divided by 0
			weight = 1 / (d + 1e-7)
			votes[pos] = votes[pos] + weight
			# print "Observation %d in dataset with distance %f votes %f for location: %s" % (r, d, weight, img_list[pos].geo)			

	# assign final vote value to img
	for v, img in zip(votes, img_list):
		img.weight = v
		# if v > 0:
		# 	print "%s %d has vote %d" % (img.location.geo, img.cameraPara.heading, v)

	fh.writeList(votes, file_path + "vote.txt")

	maxWeight = img_list[votes.argmax(axis=0)]

	return img_list, votes, maxWeight

def plotMap(img_list):
	# Plot vote map
	geo_list = [img.location.geo for img in img_list]
	mt.plot3D([geo[0] for geo in geo_list], [geo[1] for geo in geo_list], [img.weight for img in img_list])

def main(queryPath, queryDataset, extractFeature, FLANN, detector, isBRIEF):
	if queryPath == None:
		query = initQuery(obj.Location([40.693900, -73.983377], 0), obj.CameraPara(size=(800, 800), fov=120, heading=225, pitch=10))
		queryPath = query.filePath

	if queryDataset:
		pt_list = mt.hexagon(query.location.geo, 0.0005, 0.0001) # Generate sample point list
		hh.buildDataset(file_path + "image/dataset/", pt_list, obj.CameraPara(size=(800, 800), fov=120, heading=[0, 90, 180, 270], pitch=10)) # Download dataset images
	
	img_list =  fh.extractImageParas(file_path + "image/dataset/", ".jpeg")


	_, des_test, _ = ftr.featureExtraction(detector, isBRIEF, queryPath) # feature extraction for query

	if extractFeature:
		_, des_list = ftr.patchExtraction(file_path + "image/dataset/", detector, isBRIEF, ".jpeg") # Extract features from images and write the features into file
		fh.writeList(des_list, file_path + "%s%s_set.txt" % ('B' if isBRIEF else '', detector)) # Write extracted features into file
	else:
		des_list = fh.readList(file_path + "%s%s_set.txt" % ('B' if isBRIEF else '', detector)) # Read pre-extracted features from file


	# Feature Registration
	# result: size(testset) x K
	# dist: size(testset) x K
	if FLANN:		
		args = {'algorithm': 'kmeans', 'branching': 32, 'iterations': 12, 'checks': 10}
		result, dist = rgstr.FLANN(numpy.vstack(des_list), numpy.array(des_test), 3, args)
		fh.writeList(result, file_path + "%s%s_result.txt" % ('B' if isBRIEF else '', detector)) # Write extracted features into file
		fh.writeList(dist, file_path + "%s%s_dist.txt" % ('B' if isBRIEF else '', detector)) # Write extracted features into file
	else:
		result = fh.readList(file_path + "%s%s_result.txt" % ('B' if isBRIEF else '', detector)) # Read pre-extracted features from file
		dist = fh.readList(file_path + "%s%s_dist.txt" % ('B' if isBRIEF else '', detector)) # Read pre-extracted features from file

	img_list, votes, maxWeight = neighborVoting(des_list, img_list, result, dist)

	print (maxWeight.location.geo, maxWeight.cameraPara.heading, maxWeight.weight)

	# plotMap(img_list)
	mt.plotMultiWeights(img_list, [0, 90, 180, 270])
	

if __name__ == '__main__':
	# main()
	main(queryPath=None, queryDataset=False, extractFeature=False, FLANN=True, detector='SURF', isBRIEF=True)
	

	



