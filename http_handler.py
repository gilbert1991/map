import requests
import file_handler as fh

# Google stree view api 
api_base = "https://maps.googleapis.com/maps/api/streetview"
# Google api key
api_key = "AIzaSyAy8rcIJOZVRW4gGNvwkkGYv3x0ZJqC2IU"

# Encode custom api arguments
def encodeArgs(location=None, size=(800, 800), fov=120, heading=90, pitch=0):
	query_args = { 	# location can be string or (lat, lng) pair
					'location': location if isinstance(location, str) else '%f, %f' % (location[0], location[1]),
					# (width x height), default 800 x 800
					'size': '%dx%d' % size,
					'fov': fov,
					'heading': heading,
					'pitch': pitch,
					'key': api_key }

	return query_args

# Send Http GET request with encoded argument
def getImg(encoded_args):
	response = requests.get(api_base, encoded_args, stream=True)
	if response.status_code != 200:
		print "Request http error: %d" % response.status_code
	else:
		return response

# Identify image in a circle area centered at center(lat, lng) with radius(meter)
# interval(lat_interval, lng_interval)
def buildDataset(dataset_path, point_list, cameraPara = None):
	for pt in point_list:
		# Format file name with parameters
		file_name = '%s%f_%f_%d.jpeg' % (dataset_path, pt.geo[0], pt.geo[1], cameraPara.heading)

		# Encode http post parameters
		encoded_args = encodeArgs(pt.geo, cameraPara.size, cameraPara.fov, cameraPara.heading, cameraPara.pitch)

		# Http Request and Save file as file_name
		fh.img2File(getImg(encoded_args), file_name)

	print "Build dataset of %d images" % len(point_list)


if __name__ == '__main__':
	origin = [40.69415,-73.98329]
	encoded_args = encodeArgs(origin, size=(800, 800), fov=120, heading=90, pitch=10);
	fh.img2File(getImg(encoded_args), file_path + "test_2.jpeg") # Load starting image





 