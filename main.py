import matplotlib.pyplot as plt
import numpy

import http_handler as hh
import file_handler as fh
import my_util as mt
import objects as obj
import register as rgstr
import feature as ftr

file_path = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/"

def queryImage(location, cameraPara):
	# 1. Initialize the fields of query image 
	query = obj.Image()
	query.location = location # Starting GPS
	query.cameraPara = cameraPara
	query.filePath = file_path + "image/test/test.jpeg"

	# Load query image
	if cameraPara != None:
		encoded_args = hh.encodeArgs(query.location.geo, query.cameraPara);
		fh.img2File(hh.getImg(encoded_args), query.filePath)

	return query

def sampleLocation(query, radius, interval, cameraPara):
	# 2. Generate priority list of sample locations
	pt_list = mt.hexagon(query.location.geo, radius, interval)
	# Load all images in the list of sample locations

	if cameraPara != None:
		hh.buildDataset(file_path + "image/dataset/", pt_list, cameraPara)

	return pt_list

def featureExtraction(fromFile=False):
	# 3. Feature Extraction 	
	if not(fromFile):
		_, des_test = ftr.siftExtraction(file_path + "image/test/test.jpeg") # query image
		kp_list, des_list = ftr.patchExtraction(file_path + "image/dataset/", ".jpeg") # dataset images
		fh.writeList(des_list, file_path + "sift_des.txt")
		# fh.writeList(kp_list, file_path + "sift_kp.txt")
	else:
		_, des_test = ftr.siftExtraction(file_path + "image/test/test.jpeg") # query image
		des_list = fh.readList(file_path + "sift_des.txt")
		# kp_list = fh.readList(file_path + "sift_kp.txt")

	return des_test, des_list

def featureRegistration(dataset, testset):
	# Feature Registration
	args = {'algorithm': 'kmeans', 'branching': 32, 'iterations': 12, 'checks': 10}
	result, dist = rgstr.FLANN(dataset, testset, 3, args)

	return result, dist

def neighborVoting(pt_list, result, dist):
	# Create list of #des in each image to indicate the  
	index = [0]
	for des in des_list: 
		index.append(index[-1] + len(des))
	index.pop(0)

	# Voting with the distances
	votes = numpy.zeros(len(pt_list))

	for rslt, dt in zip(result, dist):		
		for r, d in zip(rslt, dt):
			pos = numpy.searchsorted(index, r)

			# Add a small value to dist to avoid divided by 0
			weight = 1 / (d + 1e-7)
			votes[pos] = votes[pos] + weight
			# print "Observation %d in dataset with distance %f votes %f for location: %s" % (r, d, weight, pt_list[pos].geo)			

	for v, pt in zip(votes, pt_list):
		if v != 0:
			print "%s has vote %d" % (pt.geo, v)

	fh.writeList(votes, file_path + "vote.txt")

	maxWeight = pt_list[votes.argmax(axis=0)]

	return votes, maxWeight

def plotMap(pt_list, votes):
	# Plot vote map
	geo_list = [pt.geo for pt in pt_list]
	mt.plot3D([geo[0] for geo in geo_list], [geo[1] for geo in geo_list], votes)


if __name__ == '__main__':
	
	# query = queryImage(obj.Location([40.69435,-73.98329], 0), obj.CameraPara(size=(800, 800), fov=100, heading=180, pitch=10))
	query = queryImage(obj.Location([40.69435,-73.98329], 0), None)

	pt_list = sampleLocation(query, 0.0005, 0.0001, obj.CameraPara(size=(800, 800), fov=100, heading=180, pitch=10)) # Load images from server
	# pt_list = sampleLocation(query, 0.0008, 0.0001, None) # Use pre-loaded images

	des_test, des_list = featureExtraction(False) # Extract features from images
	# des_test, des_list = featureExtraction(True) # Read pre-extracted features from file

	# result: size(testset) x K
	# dist: size(testset) x K
	result, dist = featureRegistration(numpy.vstack(des_list), numpy.array(des_test))

	votes, maxWeight = neighborVoting(pt_list, result, dist)

	print maxWeight.geo
	
	# votes = fh.readList(file_path + "vote.txt")
	plotMap(pt_list, votes)

	

	



