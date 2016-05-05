import pyflann as pfl
import numpy as np
import pyopengv
import cv2

import feature

# Fast Library for Approximation Nearest Neighbots
# kwargs: algorithm, branching, iter, checks
# iteration = -1 means iterate untial Kmeans converges
def FLANN(dataset, testset, K, kwargs):
	flann = pfl.FLANN()

	print "Start FLANN: K=%d, %s" % (K, kwargs)
	print "Dataset size: %d; Query size: %d" % (len(dataset), len(testset))
	result,dists = flann.nn(dataset, testset, K, **kwargs)

	return result, dists

def positionEstimation(referPosition, referRotation, relativePosition, relativeRotation):
	queryRotation = referRotation.dot(np.linalg.inv(referRotation)).T
	queryPosition = referPosition - np.linalg.inv(queryRotation.T).dot(relativePosition)

	return  queryPosition, queryRotation

def relativePositionEstimation(imgPath1, imgPath2):
	img1, img2 = cv2.imread(imgPath1, 0), cv2.imread(imgPath2, 0)

	kps1, des1 = feature.siftExtraction(img1)
	kps2, des2 = feature.siftExtraction(img2)

	matches = bruteForceMatch(des1, des2, 0.3)

	point1, point2 = extractMatchPoints(kps1, kps2, matches)

	point1 = np.array(point1)
	point2 = np.array(point2)

	# print point1
	# print point1-point2

	T = pyopengv.relative_pose_ransac(point1, point2, "NISTER", 0.01, 1000)
	R = T[:, :3]
	t = T[:, 3]

	return R, t

def bruteForceMatch(des1, des2, ratio, k=2):
	# BFMatcher with default params
	bf = cv2.BFMatcher()
	# matches[0][0] - distance, trainIdx, queryIdx, imgIdx
	matches = bf.knnMatch(des1, des2, k) # k-nearest

	# Apply ratio test
	good = []
	for m,n in matches:
		if m.distance < ratio*n.distance:
			good.append([m])

	return good

def extractMatchPoints(kp1, kp2, matches):
	point1, point2 = [], []

	for m in matches:
		idx1 = m[0].queryIdx
		idx2 = m[0].trainIdx

		(x1,y1) = kp1[idx1].pt
		(x2,y2) = kp2[idx2].pt

		point1.append([x1, y1])
		point2.append([x2, y2])

	return point1, point2

def twoViewReconstruction(p1, p2, c1, c2, threshold):
	# 1000 is #iteration
    T = pyopengv.relative_pose_ransac(p1, p2, "NISTER", threshold, 1000)
    R = T[:, :3]
    t = T[:, 3]
    inliers = _two_view_reconstruction_inliers(b1, b2, R, t, threshold)

    T = run_relative_pose_optimize_nonlinear(b1[inliers], b2[inliers], t, R)
    R = T[:, :3]
    t = T[:, 3]
    inliers = _two_view_reconstruction_inliers(b1, b2, R, t, threshold)

    return cv2.Rodrigues(R.T)[0].ravel(), -R.T.dot(t), inliers


if __name__ == '__main__':
	dataset = nr.rand(20, 4)
	testset = nr.rand(5, 4)

	args = {'algorithm': 'kmeans', 'branching': 32, 'iterations': 9, 'checks': 10}
	result, dists = FLANN(dataset, testset, 2, args)
	
	for ds in dataset: print ds
	for ts in testset: print ts
	for rlt in result: print rlt
	for dt in dists: print dt
