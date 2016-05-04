import matplotlib.pyplot as plt
import numpy

import http_handler as hh
import file_handler as fh
import my_util as mt
import objects as obj
import register as rgstr
import feature as ftr
import vote as vt
import setting as st


headings = [0, 90, 180, 270] 

def plotMap(img_list):
	# Plot vote map
	geo_list = [img.location.geo for img in img_list]
	mt.plot3D([geo[0] for geo in geo_list], [geo[1] for geo in geo_list], [img.weight for img in img_list])

def main(queryImage, queryDataset, extractFeature, FLANN, detector, isBRIEF):
	# Load query image and extract 'detector' feature 
	if isinstance(queryImage, obj.Image):
		location  = queryImage.location
		cameraPara = queryImage.cameraPara

		encoded_args = hh.encodeStreetArgs(location.geo, cameraPara.size, cameraPara.fov, cameraPara.heading, cameraPara.pitch);
		fh.img2File(hh.getStreetView(encoded_args), queryImage.filePath) # Load Image

		_, des_query, _ = ftr.featureExtraction(detector, isBRIEF, queryImage.filePath) # feature extraction for query
	elif isinstance(queryImage, str):
		_, des_query, _ = ftr.featureExtraction(detector, isBRIEF, queryImage) # feature extraction for query
	else:
		print 'Query image format error'

	
	# Load dataset images from server and extract 'detector' features
	if queryDataset:
		fh.cleanDir(st.path + "image/dataset/", ".jpeg")
		# pt_list = mt.hexagon(query.location.geo, 0.0002, 0.0001) # Generate sample point list
		network = mt.snapRoadNetwork(queryImage.location.geo, 0.0005, 0.0001)
		# mt.plotNetwork(network)
		pt_list = [pt for path in network for pt in path]
		# Download dataset images
		hh.buildDataset(st.path + "image/dataset/", pt_list, obj.CameraPara(size=(800, 800), fov=120, heading=headings, pitch=10)) 
	
	img_list =  fh.extractImageParas(st.path + "image/dataset/", ".jpeg", 7) # 7 is the number of paras contained in file names


	if extractFeature:
		_, des_dataset = ftr.patchExtraction(st.path + "image/dataset/", detector, isBRIEF, ".jpeg") # Extract features from images and write the features into file
		fh.writeList(des_dataset, st.path + "%s%s_set.txt" % ('B' if isBRIEF else '', detector)) # Write extracted features into file
	else:
		des_dataset = fh.readList(st.path + "%s%s_set.txt" % ('B' if isBRIEF else '', detector)) # Read pre-extracted features from file


	# Feature Registration
	# result: size(des_query) x K
	# dist: size(des_query) x K
	if FLANN:		
		args = {'algorithm': 'kmeans', 'branching': 32, 'iterations': 12, 'checks': 10}
		result, dist = rgstr.FLANN(numpy.vstack(des_dataset), numpy.array(des_query), 3, args)
		fh.writeList(result, st.path + "%s%s_result.txt" % ('B' if isBRIEF else '', detector)) # Write extracted features into file
		fh.writeList(dist, st.path + "%s%s_dist.txt" % ('B' if isBRIEF else '', detector)) # Write extracted features into file
	else:
		result = fh.readList(st.path + "%s%s_result.txt" % ('B' if isBRIEF else '', detector)) # Read pre-extracted features from file
		dist = fh.readList(st.path + "%s%s_dist.txt" % ('B' if isBRIEF else '', detector)) # Read pre-extracted features from file



	img_list, votes, maxImage = vt.neighborVoting(des_dataset, img_list, result, dist)

	analysis = vt.analysisHeadingWeights(img_list, headings)
	# print (maxImage.location.geo, maxImage.cameraPara.heading, maxImage.weight)


	# plotMap(img_list)
	# mt.plotMultiWeights(img_list, headings, maxImage.weight)

	# fh.showImage(queryImage.filePath)
	

if __name__ == '__main__':
	queryImage = obj.Image(obj.Location([40.693903, -73.983434], 0), 
					obj.CameraPara(size =(800, 800), fov = 120, heading = 90, pitch = 0),
						st.path + 'image/query.jpeg')

	# main(queryImage=queryImage, queryDataset=True, extractFeature=True, FLANN=True, detector='SIFT', isBRIEF=False)
	main(queryImage=queryImage, queryDataset=False, extractFeature=False, FLANN=False, detector='SIFT', isBRIEF=False)

	

	



