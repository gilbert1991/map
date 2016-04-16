import cv2
import numpy as np

import file_handler as fh
import setting as st

def featureExtraction(detector, isBRIEF, img_in, img_out=None):
	img = cv2.imread(img_in, 0)

	if detector == 'SIFT':
		kps, des = siftExtraction(img)
	elif detector == 'SURF':
		kps, des = surfExtraction(img)
	else:
		raise AttributeError('%s is not defined in featureExtraction()' % detector)

	if isBRIEF:
		kps, des = briefExtraction(kps, img)

	# Extract the CV data structure as list of dictionary
	points = []
	for kp in kps:
		p = {'pt': kp.pt, 'size': kp.size, 'angle': kp.angle, 'response': kp.response, 'octave': kp.octave, 'id': kp.class_id}
		points.append(p)

	# Draw key points if output path specified
	if img_out:
		img = cv2.drawKeypoints(img, kps, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imwrite(img_out, img)

	print '%s extracted%sfor %s' % (detector, ' with BRIEF ' if isBRIEF else ' ', fh.path_leaf(img_in))

	return kps, des, points


# Feature Extraction
# kp - pt, size, andgle, response, octave
# des - N x 128
def siftExtraction(img):
	sift = cv2.SIFT(contrastThreshold=0.06)

	kps, des = sift.detectAndCompute(img, None)		

	return kps, des

def surfExtraction(img):
	# Create SURF object. You can specify params here or later.
	# Here I set Hessian Threshold to 400
	surf = cv2.SURF(400)
	
	# Find keypoints and descriptors directly
 	kps, des = surf.detectAndCompute(img, None)	

	return kps, des

def briefExtraction(kps, img):	
	# Initiate BRIEF extractor
	brief = cv2.DescriptorExtractor_create("BRIEF")

	# compute the descriptors with BRIEF
	kps, des = brief.compute(img, kps)

	return kps, des

# Feature Extraction of dataset
def patchExtraction(data_path, detector, isBRIEF=False, file_ext=None):
	print "Extracting patch %s detectors..." % detector

	kp_list = []
	des_list = []

	f_list = fh.listFiles(data_path, file_ext)
	
	for f in f_list:
		kp, des, points = featureExtraction(detector, isBRIEF, f)
		kp_list.append(kp)
		des_list.append(des)			

	return kp_list, des_list


if __name__ == '__main__':
	dataset = st.path + "image/dataset"
	img = st.path + "image/test/test.jpeg"
	sift = st.path + "image/test/test_sift.jpeg"
	surf = st.path + "image/test/test_surf.jpeg"
	brief = st.path + "image/test/test_brief.jpeg"

	featureExtraction('SIFT', False, img, sift)
