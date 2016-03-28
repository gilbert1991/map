import math
from decimal import Decimal

# Convert geo coords (lat, lng) diff to distance in meters
def geo2dist(origin, geo_diff):
	distance = []

	distance.append(40075160 * math.cos(math.radians(origin[0])))
	distance.append(origin[1] * 40008000 / 360)
	
	return distance

# Convert distance diff (lat_meter, lng_meter) to geo coords
def dist2geo(origin, dist_diff):
	coords = []
	coords.append(dist_diff[0] / (40075160.0 * math.cos(math.radians(origin[0])).real))
	# coords.append(dist_diff[1] * 360 / 40008000)
	coords.append(dist_diff[1] * 360.0 / 40008000.0)

	return coords

# def lat_circumference(lat):
# 	lat_circum = lat * math.pi / 180
# 	return lat_circum