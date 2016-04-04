import matplotlib.pyplot as plt

import http_handler as hh
import file_handler as fh
import my_util as mt
import image
import register as rgstr
import feature as ftr

file_path = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/"

if __name__ == '__main__':
	# Load the query image with 'geo' and 'params'
	origin = [40.69435,-73.98329] # Starting GPS
	encoded_args = hh.encodeArgs(origin);
	fh.img2File(hh.getImg(encoded_args), file_path + "image/test/test.jpeg") # Load starting image
	
	# Generate priority list of sample locations
	pt_list = mt.hexagon(origin, 0.0003, 0.00005)
	# Load all images in the list of sample locations
	hh.buildDataset(file_path + "image/dataset/", pt_list, image.CameraPara((800, 800), 120, 90, 10))

	# Feature Extraction 
	ftr.patchExtraction(file_path + "image/dataset/", ".jpeg") # dataset images
	kp, des = ftr.siftExtraction(file_path + "image/test/test.jpeg") # query image

	# Feature Registration
	# result, dist = rgstr.FLANN()