import matplotlib.pyplot as plt

import http_handler as hh
import file_handler as fh
import my_util as mu
import image
import register as rgstr

file_path = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test/"

# Identify image in a circle area centered at center(lat, lng) with radius(meter)
# interval(lat_interval, lng_interval)
def buildDataset(point_list, cameraPara = None):
	for pt in point_list:
		# Format file name with parameters
		file_name = '%s%f_%f_%d.jpg' % (file_path, pt.geo[0], pt.geo[1], cameraPara.heading)

		# Encode http post parameters
		encoded_args = hh.encodeArgs(pt.geo, 
			cameraPara.size, cameraPara.fov, cameraPara.heading, cameraPara.pitch)

		# Http Request and Save file as file_name
		fh.img2File(hh.getImg(encoded_args), file_name)


if __name__ == '__main__':
	# Starting GPS
	origin = [40.69455,-73.98329]
	encoded_args = hh.encodeArgs(origin);
	fh.img2File(hh.getImg(encoded_args), file_path + "test_2.jpeg") # Load starting image
	
	# Generate priority list of sample locations
	pt_list = mu.hexagon(origin, 0.0003, 0.00005)
	# Load images in the list of sample locations
	buildDataset(pt_list, image.CameraPara((800, 800), 120, 90, 10))

	# Feature Extraction

	# Feature Registration
	result, dist = rgstr.FLANN()