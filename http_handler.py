import requests
import file_handler as fh

# Google stree view api 
api_base = "https://maps.googleapis.com/maps/api/streetview"
# Google api key
api_key = "AIzaSyAy8rcIJOZVRW4gGNvwkkGYv3x0ZJqC2IU"

# Encode custom api arguments
def encodeArgs(location, size, fov, heading, pitch):
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
	count = 0 

	for pt in point_list:

		for heading in cameraPara.heading:

			# Format file name with parameters
			file_name = '%s%f_%f_%d_%d_%d_%d_%d_%d.jpeg' % (dataset_path, pt.geo[0], pt.geo[1], 
				pt.layer, cameraPara.size[0], cameraPara.size[1], cameraPara.fov, heading, cameraPara.pitch)

			# Encode http post parameters
			encoded_args = encodeArgs(pt.geo, cameraPara.size, cameraPara.fov, heading, cameraPara.pitch)

			# Http Request and Save file as file_name
			fh.img2File(getImg(encoded_args), file_name)

			count = count + 1

	print "Build dataset of %d images" % count


if __name__ == '__main__':
	origin = [40.69415,-73.98329]
	# encoded_args = encodeArgs([40.69435, -73.98329], size=(800, 800), fov=100, heading=[0, 90, 180, 270], pitch=10);
	# fh.img2File(getImg(encoded_args), file_path + "test_2.jpeg") # Load starting image





 