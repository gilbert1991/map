import cv2
import numpy as np

# Feature Extraction
def siftExtraction(img_in, img_out):
	img = cv2.imread(img_in)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	sift = cv2.SIFT()
	kp, des = sift.detectAndCompute(gray, None)

	img = cv2.drawKeypoints(gray, kp, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	cv2.imwrite(img_out, img)

	return kp, des


if __name__ == '__main__':
	img = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test/test.jpeg"
	sift = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test/test_sift.jpeg"

	kp, des = siftExtraction(img, sift)

	count = 0
	for d in des:
		count += 1
		print len(d)

	print count