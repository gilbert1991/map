import cv2
import numpy as np
import file_handler as fh

# Feature Extraction
# kp - pt, size, andgle, response, octave
# des - N x 128
def siftExtraction(img_in, img_out=None):
	img = cv2.imread(img_in)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	sift = cv2.SIFT()
	kp, des = sift.detectAndCompute(gray, None)

	# Draw key points if output path specified
	if img_out:
		img = cv2.drawKeypoints(img, kp, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imwrite(img_out, img)

	return kp, des

# Feature Extraction of dataset
def patchExtraction(data_path, file_ext=None):
	features = []

	f_list = fh.listFiles(data_path, file_ext)

	for f in f_list:
		print f



if __name__ == '__main__':
	dataset = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/dataset"
	img = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test/test_1.jpeg"
	sift = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test/test_1_sift.jpeg"

	# kp, des = siftExtraction(img)
	patchExtraction(dataset, "jpeg")