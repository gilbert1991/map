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
	kps, des = sift.detectAndCompute(gray, None)

	# Draw key points if output path specified
	if img_out:
		img = cv2.drawKeypoints(img, kps, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imwrite(img_out, img)

	point = []
	for kp in kps:
		p = {'pt': kp.pt, 'size': kp.size, 'angle': kp.angle, 'response': kp.response, 'octave': kp.octave, 'id': kp.class_id}
		point.append(p)

	return point, des

# Feature Extraction of dataset
def patchExtraction(data_path, file_ext=None):
	kp_list = []
	des_list = []

	f_list = fh.listFiles(data_path, file_ext)

	for f in f_list:
		print f
		kp, des = siftExtraction(f)
		kp_list.append(kp)
		des_list.append(des)

	return kp_list, des_list#



if __name__ == '__main__':
	dataset = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/dataset"
	img = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test/test.jpeg"
	sift = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test/test_1_sift.jpeg"

	point, des = siftExtraction(img)
	print point[0]

	# patchExtraction(dataset, "jpeg")