import http_handler as hh
import file_handler as fh
import my_util as mu
import matplotlib.pyplot as plt
import image

file_path = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/"

# Identify image in a circle area centered at center(lat, lng) with radius(meter)
# interval(lat_interval, lng_interval)
def find_in_range(point_list, cameraPara = None):
	for pt in point_list:
		# Format file name with parameters
		# file_name = file_path.join([
		# 	pt.geo[0], '_', 
		# 	pt.geo[1], '_', 
		# 	cameraPara.heading, 
		# 	'.jpg'])
		file_name = '%s%f_%f_%d.jpg' % (file_path, pt.geo[0], pt.geo[1], cameraPara.heading)

		# Encode http post parameters
		encoded_args = hh.encode_args(pt.geo, 
			cameraPara.size, cameraPara.fov, cameraPara.heading, cameraPara.pitch)

		# Http Request and Save file as file_name
		fh.img2file(hh.get_img(encoded_args), file_name)


if __name__ == '__main__':
	origin = [40.69435,-73.98329]

	# encoded_args = http_handler.encode_args(origin);
	# file_path = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test.jpeg"

	# file_handler.img2file(http_handler.get_img(encoded_args), file_path)
	
	pt_list = mu.hexagon(origin, 0.0003, 0.00005)

	find_in_range(pt_list, image.CameraPara((800, 800), 120, 90, 10))