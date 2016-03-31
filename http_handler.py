import requests

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





 