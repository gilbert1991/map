import requests
import json

import file_handler as fh

# Google map api 
street_view_base = "https://maps.googleapis.com/maps/api/streetview"
snap_road_base = "https://roads.googleapis.com/v1/snapToRoads"
# Google api key
street_view_key = "AIzaSyAy8rcIJOZVRW4gGNvwkkGYv3x0ZJqC2IU"
snap_road_key = "AIzaSyBYkXXULu2MoMzpS48_DPQ1u2tt8UNREsg"

# Snap to road from list of points
def snapToRoad(path):
	print 'Snap to road %s' % path

	encoded_args = { 
					'path': "|".join("%f,%f" % geo for geo in path),
					'interpolate': 'true',
					'key': snap_road_key }

	response = requests.get(snap_road_base, encoded_args)

	if response.status_code != 200:
		print "Request http error: %d" % response.status_code
	else:
		return json.loads(response.text)

# Encode street view api arguments
def encodeStreetArgs(location, size, fov, heading, pitch):
	query_args = { 	# location can be string or (lat, lng) pair
					'location': location if isinstance(location, str) else '%f, %f' % (location[0], location[1]),
					# (width x height), default 800 x 800
					'size': '%dx%d' % size,
					'fov': fov,
					'heading': heading,
					'pitch': pitch,
					'key': street_view_key }

	return query_args

# get street view image from StreetView server
def getStreetView(encoded_args):
	response = requests.get(street_view_base, encoded_args, stream=True)
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
			encoded_args = encodeStreetArgs(pt.geo, cameraPara.size, cameraPara.fov, heading, cameraPara.pitch)

			# Http Request and Save file as file_name
			fh.img2File(getStreetView(encoded_args), file_name)

			count = count + 1

	print "Build dataset of %d images" % count

def parseJsonRoad(road):
	locations = []

	if 'snappedPoints' in road:
		places = road['snappedPoints']		
		for p in places:		
			locations.append((p['location']['latitude'], p['location']['longitude']))
	else:
		print 'Snapped Points not exist'

	return locations

if __name__ == '__main__':
	path = [(-35.27801,149.12958),(-35.28032,149.12907),(-35.28099,149.12929),(-35.28144,149.12984),(-35.28194,149.13003),(-35.28282,149.12956)]
	road = snapToRoad(path)
	a = json.dumps(road, indent=4)
	print parseJsonRoad(road)
	# encoded_args = encodeArgs([40.69435, -73.98329], size=(800, 800), fov=100, heading=[0, 90, 180, 270], pitch=10);
	# fh.img2File(getImg(encoded_args), file_path + "test_2.jpeg") # Load starting image





 