import http_handler as hh
import file_handler as fh
import my_util as mu
import matplotlib.pyplot as plt
import image

file_path = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test/"

# Identify image in a circle area centered at center(lat, lng) with radius(meter)
# interval(lat_interval, lng_interval)
def findRange(point_list, cameraPara = None):
	for pt in point_list:
		# Format file name with parameters
		file_name = '%s%f_%f_%d.jpg' % (file_path, pt.geo[0], pt.geo[1], cameraPara.heading)

		# Encode http post parameters
		encoded_args = hh.encodeArgs(pt.geo, 
			cameraPara.size, cameraPara.fov, cameraPara.heading, cameraPara.pitch)

		# Http Request and Save file as file_name
		fh.img2File(hh.getImg(encoded_args), file_name)


if __name__ == '__main__':
	origin = [40.69435,-73.98329]

	encoded_args = hh.encodeArgs(origin);

	fh.img2File(hh.getImg(encoded_args), file_path + "test.jpeg")
	
	# pt_list = mu.hexagon(origin, 0.0003, 0.00005)

	# findRange(pt_list, image.CameraPara((800, 800), 120, 90, 10))