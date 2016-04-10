import pyflann as pfl
import numpy.random as nr

# Fast Library for Approximation Nearest Neighbots
# kwargs: algorithm, branching, iter, checks
# iteration = -1 means iterate untial Kmeans converges
def FLANN(dataset, testset, K, kwargs):
	flann = pfl.FLANN()

	print "Start FLANN: K=%d, %s" % (K, kwargs)
	print "Dataset size: %d; Query size: %d" % (len(dataset), len(testset))
	result,dists = flann.nn(dataset, testset, K, **kwargs)

	return result, dists


if __name__ == '__main__':
	dataset = nr.rand(20, 4)
	testset = nr.rand(5, 4)

	args = {'algorithm': 'kmeans', 'branching': 32, 'iterations': 9, 'checks': 10}
	result, dists = FLANN(dataset, testset, 2, args)
	
	for ds in dataset: print ds
	for ts in testset: print ts
	for rlt in result: print rlt
	for dt in dists: print dt
