import matplotlib.pyplot as plt
import numpy

import http_handler as hh
import file_handler as fh
import my_util as mt
import objects as obj
import register
import feature as ftr
import vote 
import setting as st

def plotMap(img_list):
	# Plot vote map
	geo_list = [img.position for img in img_list]
	mt.plot3D([geo[0] for geo in geo_list], [geo[1] for geo in geo_list], [img.weight for img in img_list])

def initQuery(queryImage, detector, isBRIEF):
	print 'Start init query image'
	# Load query image and extract 'detector' feature 
	if queryImage.filePath is None:
		queryImage.filePath = st.path + 'image/query/test.jpeg'
		
		cameraPara = queryImage.cameraPara
		encoded_args = hh.encodeStreetArgs(queryImage.position, cameraPara.size, cameraPara.fov, cameraPara.heading, cameraPara.pitch);
		fh.img2File(hh.getStreetView(encoded_args), queryImage.filePath) # Load Image

		print 'Loaded image from Google StreetView'

	else:
		width, height = mt.resizeImage(queryImage.filePath, queryImage.filePath, [800, 800])
		queryImage.cameraPara.size = (width, height)

		print 'Loaded image from %s and resized image to %s' % (queryImage.filePath, queryImage.cameraPara.size)


	_, des_query, _ = ftr.featureExtraction(detector, isBRIEF, queryImage.filePath) # feature extraction for query

	return des_query

def buildDataset(queryImage, dataType, dataPath, headings, detector, isBRIEF):
	print 'Start building dataset'

	featureFilePath = st.path + "%s%s_set.txt" % ('B' if isBRIEF else '', detector)
	dataSetCameraPara = queryImage.cameraPara
	dataSetCameraPara.heading = headings

	# Load dataset images from server and extract 'detector' features
	if dataType == 'LOCAL':
		network = mt.snapRoadNetwork(queryImage.position, 0.0005, 0.0001)
		pt_list = [pt for path in network for pt in path]

		fh.cleanDir(dataPath, ".jpeg")	
		hh.buildDataset(dataPath, pt_list, dataSetCameraPara)	

		_, des_dataset = ftr.patchExtraction(dataPath, detector, isBRIEF, ".jpeg") # Extract features from images and write the features into file
		fh.writeList(des_dataset, featureFilePath) # Write extracted features into file

	elif dataType == 'ORIENT':
		fh.cleanDir(dataPath, ".jpeg")
		hh.buildDataset(dataPath, [queryImage.position], dataSetCameraPara)

		_, des_dataset = ftr.patchExtraction(dataPath, detector, isBRIEF, ".jpeg") # Extract features from images and write the features into file
		fh.writeList(des_dataset, featureFilePath) # Write extracted features into file

	else:
		des_dataset = fh.readList(featureFilePath) # Read pre-extracted features from file

	img_list =  fh.extractImageParas(dataPath, ".jpeg", 7) # 7 is the number of paras contained in file names

	return img_list, des_dataset

def matching(des_query, des_dataset, method, K, detector, isBRIEF):
	print 'Start matching query and dataset features'

	resultFilePath = st.path + "%s%s_result.txt" % ('B' if isBRIEF else '', detector)
	distFilePath = "%s%s_dist.txt" % ('B' if isBRIEF else '', detector)

	# result: size(des_query) x K
	# dist: size(des_query) x K
	if method == 'FLANN':		
		args = {'algorithm': 'kmeans', 'branching': 32, 'iterations': 12, 'checks': 10}
		result, dist = register.FLANN(numpy.vstack(des_dataset), numpy.array(des_query), K, args)
		fh.writeList(result, resultFilePath) # Write extracted features into file
		fh.writeList(dist, distFilePath) # Write extracted features into file
	elif method == 'BRUTE':
		register.bruteForceMatch(des_query, des_dataset, 0.3, K=2)
	else:
		result = fh.readList(resultFilePath) # Read pre-extracted features from file
		dist = fh.readList(distFilePath) # Read pre-extracted features from file

	return result, dist

def main():
	detector, isBRIEF = 'SIFT', False

	queryImage = obj.Image(
		position=[40.693903, -73.983434], 
		cameraPara=obj.CameraPara(size =(800, 800), fov = 100, heading = 90, pitch = 20),
		filePath=st.path + 'image/query/IMG_4352.JPG')

	# Localization
	# des_query = initQuery(queryImage, detector, isBRIEF)
	# img_list, des_dataset = buildDataset(queryImage, 'LOCAL', st.path + 'image/local/', headings, detector, isBRIEF)
	# result, dist = matching(des_query, des_dataset, 'FLANN', 2, detector, isBRIEF)
	# img_list, votes, maxImage = vote.neighborVoting(des_dataset, img_list, result, dist)
	# # analysis = vote.analysisHeadingWeights(img_list, headings)
	# print (maxImage.position, maxImage.cameraPara.heading, maxImage.weight)


	# Orientation Estimation
	des_query = initQuery(queryImage, detector, isBRIEF)

	headings = [queryImage.cameraPara.heading + dev * 10 for dev in range(-1, 2)]
	img_list, des_dataset = buildDataset(queryImage, 'ORIENT', st.path + 'image/orient/', headings, detector, isBRIEF)
	result, dist = matching(des_query, des_dataset, 'FLANN', 2, detector, isBRIEF)
	img_list, votes, maxImage = vote.neighborVoting(des_dataset, img_list, result, dist)
	# analysis = vote.analysisHeadingWeights(img_list, headings)
	print (maxImage.position, maxImage.cameraPara.heading, maxImage.weight)


	# plotMap(img_list)
	# mt.plotMultiWeights(img_list, headings, maxImage.weight)

	# fh.showImage(queryImage.filePath)
	

if __name__ == '__main__':
	main()

	

	



