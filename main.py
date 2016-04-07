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

def featureExtraction():
	# 3. Feature Extraction 	
	_, des_test = ftr.siftExtraction(file_path + "image/test/test.jpeg") # query image
	kp_list, des_list = ftr.patchExtraction(file_path + "image/dataset/", ".jpeg") # dataset images
	fh.writeList(des_list, file_path + "sift_des.txt")
	# fh.writeList(kp_list, file_path + "sift_kp.txt")
	# des_list = fh.readList(file_path + "sift_des.txt")
	# kp_list = fh.readList(file_path + "sift_kp.txt")

	return des_test, des_list

def featureRegistration(dataset, testset):
	# Feature Registration
	args = {'algorithm': 'kmeans', 'branching': 32, 'iterations': 12, 'checks': 10}
	result, dist = rgstr.FLANN(dataset, testset, 3, args)

	return result, dist

def neighborVoting(pt_list, result, dist, index):
	# Voting with the distances
	votes = numpy.zeros(len(pt_list))

	# Add a small value to dist to avoid divided by 0
	dist = [ d + 1e-10 for d in dist ]

	for rslt, dt in zip(result, dist):
		position = numpy.searchsorted(index, rslt)
		weight = 1 / dt
		votes[position] = votes[position] + weight
		print (rslt, dt, position, weight)

	fh.writeList(votes, file_path + "vote.txt")

	return votes

def plotMap(pt_list, votes):
	# Plot vote map
	geo_list = [pt.geo for pt in pt_list]
	mt.plot3D([geo[0] for geo in geo_list], [geo[1] for geo in geo_list], votes)


if __name__ == '__main__':
	
	query = queryImage(obj.Location([40.69435,-73.98329], 0), obj.CameraPara(size=(800, 800), fov=100, heading=270, pitch=10))

	pt_list = sampleLocation(query, 0.0008, 0.0001, obj.CameraPara(size=(800, 800), fov=100, heading=270, pitch=10))
	# pt_list = sampleLocation(query, 0.0005, 0.0001, None)

	des_test, des_list = featureExtraction()

	# Create list of #des in each image to indicate the  
	index = [0]
	for des in des_list: 
		index.append(index[-1] + len(des))
	index.pop(0)

	result, dist = featureRegistration(numpy.vstack(des_list), numpy.array(des_test))

	votes = neighborVoting(pt_list, result, dist, index)
	votes = numpy.zeros(len(pt_list))
	votes = fh.readList(file_path + "vote.txt")
	target = pt_list[votes.argmax(axis=0)]
	print target.geo
	
	plotMap(pt_list, votes)

	

	



