import pyflann as pfl
import numpy.random as nr
import pyopengv
import cv2

# Fast Library for Approximation Nearest Neighbots
# kwargs: algorithm, branching, iter, checks
# iteration = -1 means iterate untial Kmeans converges
def FLANN(dataset, testset, K, kwargs):
	flann = pfl.FLANN()

	print "Start FLANN: K=%d, %s" % (K, kwargs)
	print "Dataset size: %d; Query size: %d" % (len(dataset), len(testset))
	result,dists = flann.nn(dataset, testset, K, **kwargs)

	return result, dists

def bruteForceMatch(des1, des2, ratio):
	# BFMatcher with default params
	bf = cv2.BFMatcher()
	matches = bf.knnMatch(des1,des2, k=2)

	# Apply ratio test
	good = []
	for m,n in matches:
		if m.distance < ratio*n.distance:
			good.append([m])

	return good


def registration(point1, point2, camera1, camera2, matches):
	twoViewReconstruction(point1, point2, camera1, camera2, 0.01)

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
