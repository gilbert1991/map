import cv2
import numpy as np

import file_handler as fh
import setting as st

# Feature Extraction
# kp - pt, size, andgle, response, octave
# des - N x 128
def siftExtraction(img_in, img_out=None):
	img = cv2.imread(img_in)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	sift = cv2.SIFT()
	kps, des = sift.detectAndCompute(gray, None)	

	# Extract the CV data structure as list of dictionary
	points = []
	for kp in kps:
		p = {'pt': kp.pt, 'size': kp.size, 'angle': kp.angle, 'response': kp.response, 'octave': kp.octave, 'id': kp.class_id}
		points.append(p)

	# Draw key points if output path specified
	if img_out:
		img = cv2.drawKeypoints(img, kps, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imwrite(img_out, img)

	print 'SIFT extracted for %s' % fh.path_leaf(img_in)

	return kps, des, points

def surfExtraction(img_in, img_out=None):
	img = cv2.imread(img_in, 0)
	
	# Create SURF object. You can specify params here or later.
	# Here I set Hessian Threshold to 400
	surf = cv2.SURF(400)
	
	# Find keypoints and descriptors directly
 	kps, des = surf.detectAndCompute(img, None)	

	# Extract the CV data structure as list of dictionary
	points = []
	for kp in kps:
		p = {'pt': kp.pt, 'size': kp.size, 'angle': kp.angle, 'response': kp.response, 'octave': kp.octave, 'id': kp.class_id}
		points.append(p)

	# Draw key points if output path specified
	if img_out:
		img = cv2.drawKeypoints(cv2.imread(img_in), kps, None, (255, 0, 0), 4)
		cv2.imwrite(img_out, img)

	print 'SURF extracted for %s' % fh.path_leaf(img_in)

	return kps, des, points

def briefExtraction(feature, img_in, img_out=None):
	if feature is None:
		print 'Please specify a feature descriptor for BRIEF'

	else:
		img = cv2.imread(img_in, 0)

		if feature == 'SIFT':
			kps, des, points = siftExtraction(img_in, img_out)
		elif feature == 'SURF':
			kps, des, points = surfExtraction(img_in, img_out)
		else:
			print 'Feature not defined in BRIEF'

		# Initiate BRIEF extractor
		brief = cv2.DescriptorExtractor_create("BRIEF")

		# compute the descriptors with BRIEF
		kps_brief, des_brief = brief.compute(img, kps)

		# Extract the CV data structure as list of dictionary
		points = []
		for kp in kps_brief:
			p = {'pt': kp.pt, 'size': kp.size, 'angle': kp.angle, 'response': kp.response, 'octave': kp.octave, 'id': kp.class_id}
			points.append(p)

		# Draw key points if output path specified
		if img_out:
			img = cv2.drawKeypoints(cv2.imread(img_in), kps, None, (255, 0, 0), 4)
			cv2.imwrite(img_out, img)

		print 'BRIEF extracted for %s' % fh.path_leaf(img_in)

		return kps_brief, des_brief, points

# Feature Extraction of dataset
def patchExtraction(data_path, feature, brief=False, file_ext=None):
	if feature is None:
		print 'Please specify a feature descriptor for BRIEF'
	
	else:
		kp_list = []
		des_list = []

		f_list = fh.listFiles(data_path, file_ext)

		print "Extracting patch %s features..." % feature
		
		# TODO: Dirty Code 
		if brief:
			for f in f_list:
				kp, des, points = briefExtraction(feature, f)
				kp_list.append(kp)
				des_list.append(des)
		elif feature == 'SIFT':
			for f in f_list:
				kp, des, points = siftExtraction(f)
				kp_list.append(kp)
				des_list.append(des)
		elif feature == 'SURF':
			for f in f_list:
				kp, des, points = surfExtraction(f)
				kp_list.append(kp)
				des_list.append(des)
		else:
			print 'Feature not defined in patchExtraction()'					

		return kp_list, des_list


if __name__ == '__main__':
	dataset = st.path + "image/dataset"
	img = st.path + "image/test/test.jpeg"
	sift = st.path + "image/test/test_sift.jpeg"
	surf = st.path + "image/test/test_surf.jpeg"
	brief = st.path + "image/test/test_brief.jpeg"

	kps, des, points = siftExtraction(img, sift)

	kps2, des2, points2 = surfExtraction(img, surf)

	kps3, des3, points3 = briefExtraction('SURF', img, brief)


	# patchExtraction(dataset, "jpeg")