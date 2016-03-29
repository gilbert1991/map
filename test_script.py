import http_handler
import file_handler
import my_util

# Identify image in a circle area centered at center(lat, lng) with radius(meter)
# interval(lat_interval, lng_interval)
def find_in_range(center, radius, interval=(10), args):
	sample_list = [center]

	size = args.get('size', (800, 800))
	fov = agrs.get('fov', 120)
	heading = args.get('heading', [0, 90, 180, 270])
	pitch = args.get('pitch', 10)



if __name__ == '__main__':
	encoded_args = http_handler.encode_args(location = [40.694305,-73.983298], None);
	file_path = "/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/test.jpeg"

	file_handler.img2file(http_handler.get_img(encoded_args), file_path)
	# print my_util.geo2dist([40.720032, -73.988354], [1, 1])
	# print my_util.dist2geo([40.720032, -73.988354], [20, 20])
