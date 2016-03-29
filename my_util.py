import geopy.distance as gpy

# Convert geo coords (lat, lng) diff to distance in meters
# lat: 0.0001 ~= 11.1m, lng 0.0001 ~= 8.5m
def geo_distance(ori, dst, method='vincenty'):
	if method == 'vincenty':
		distance = gpy.vincenty(ori, dst).meters
	elif method == 'great_circle':
		distance = gpy.great_circle(ori, dst).meters
	else:
		print('Error with geo_distance')

	return distance	

if __name__ == '__main__':
	ori = (40.69465, -73.98327)
	dst = (40.69465, -73.98337)
	print(geo_distance(ori, dst, 'great_circle'))