import matplotlib.pyplot as plt
import numpy

import http_handler as hh
import file_handler as fh
import my_util as mt
import objects as obj
import register as rgstr
import feature as ftr

file_path = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/"

if __name__ == '__main__':
	# Initialize the fields of query image 
	query = obj.Image()
	query.location = obj.Location([40.69435,-73.98329], 0)# Starting GPS
	query.cameraPara = obj.CameraPara(size=(800, 800), fov=120, heading=90, pitch=0)
	query.filePath = file_path + "image/test/test.jpeg"

	# Load query image
	# encoded_args = hh.encodeArgs(query.location.geo);
	# fh.img2File(hh.getImg(encoded_args), query.filePath) # Load starting image
	
	# Generate priority list of sample locations
	pt_list = mt.hexagon(query.location.geo, 0.0003, 0.00005)
	# Load all images in the list of sample locations
	# hh.buildDataset(file_path + "image/dataset/", pt_list, obj.CameraPara((800, 800), 120, 90, 10))

	# Feature Extraction 
	# kp_list, des_list = ftr.patchExtraction(file_path + "image/dataset/", ".jpeg") # dataset images
	# _, test = ftr.siftExtraction(file_path + "image/test/test.jpeg") # query image

	# print numpy.array(test).shape

	# fh.writeList(kp_list, file_path + "sift_kp.txt")
	# fh.writeList(des_list, file_path + "sift_des.txt")

	# # kps = fh.readList(file_path + "sift_kp.txt")
	# dess = fh.readList(file_path + "sift_des.txt")

	# index = [0]
	# for des in dess: 
	# 	index.append(index[-1] + len(des))
	# 	print index[-1]

	# index.pop(0)

	# dess = numpy.vstack(dess)

	# print dess.shape


	# # Feature Registration
	# args = {'algorithm': 'kmeans', 'branching': 32, 'iterations': 9, 'checks': 10}
	# result, dist = rgstr.FLANN(dess, numpy.array(test), 5, args)

	# votes = numpy.zeros(len(pt_list))
	# for rslt, dt in zip(result, dist):
	# 	position = numpy.searchsorted(index, rslt)
	# 	weight = 1 / dt
	# 	votes[position] = votes[position] + weight
	# 	print (rslt, dt, position, weight)

	# fh.writeList(votes, file_path + "vote.txt")
	votes = fh.readList(file_path + "vote.txt")

	geo_list = [pt.geo for pt in pt_list]
	mt.plot3D([geo[0] for geo in geo_list], [geo[1] for geo in geo_list], votes)



