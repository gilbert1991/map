import cv2
import numpy as np

# Feature Extraction
def sift_extraction(img_in, img_out):
	img = cv2.imread(img_in)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	sift = cv2.SIFT()
	kp = sift.detect(gray, None)

	img = cv2.drawKeypoints(gray, kp, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	cv2.imwrite(img_out, img)


if __name__ == '__main__':
	img = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test.jpeg"
	sift = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test_sift.jpeg"
	sift_extraction(img, sift)