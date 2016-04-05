import geopy.distance as gpy
import math

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

import objects as obj

# Convert geo coords (lat, lng) diff to distance in meters
# lat: 0.0001 ~= 11.1m, lng 0.0001 ~= 8.5m
def geoDistance(ori, dst, method='vincenty'):
	if method == 'vincenty':
		distance = gpy.vincenty(ori, dst).meters
	elif method == 'great_circle':
		distance = gpy.great_circle(ori, dst).meters
	else:
		print('Error with geo_distance')

	return distance	

# Sample Location Generation
def hexagon(origin = (0, 0), radius = 20, interval = 1):
	# init point list with origin at layer 0
	point_list = [obj.Location((origin[0], origin[1]), layer = 0)] 

	# number of layers to cover the area
	# layer is the position of a hexagon
	no_layer = int(math.ceil(radius / interval)) 

	# Generate points layer by layer 
	for lyr in range(1, no_layer + 1):
		unit_length = interval * lyr
		height_length = unit_length * math.sqrt(3) / 2

		layer_list = []

		# Create 6 vertices
		#   3 o---o 2
		#    / \ / \
		# 4 o---o---o 1
		#    \ / \ /
		#   5 o---o 6
		layer_list.append(obj.Location((origin[0] + unit_length, origin[1]), lyr)) # 1
		layer_list.append(obj.Location((origin[0] + unit_length / 2, origin[1] + height_length), lyr)) # 2
		layer_list.append(obj.Location((origin[0] - unit_length / 2, origin[1] + height_length), lyr)) # 3
		layer_list.append(obj.Location((origin[0] - unit_length, origin[1]), lyr)) # 4
		layer_list.append(obj.Location((origin[0] - unit_length / 2, origin[1] - height_length), lyr)) # 5 
		layer_list.append(obj.Location((origin[0] + unit_length / 2, origin[1] - height_length), lyr)) # 6

		# number of points on an edge exclude two vertices
		no_point_on_edge = lyr - 1 

		# Append start vertext and points on edge , edge by edge
		for edge in range(6):
			v_start = layer_list[edge]
			v_end = layer_list[(edge + 1) % 6]

			lat_diff = (v_start.geo[0] - v_end.geo[0]) / (no_point_on_edge + 1)
			lng_diff = (v_start.geo[1] - v_end.geo[1]) / (no_point_on_edge + 1)

 			point_list.append(v_start)

			for pt in range(1, no_point_on_edge + 1):
				point_list.append(obj.Location((v_start.geo[0] - pt * lat_diff, v_start.geo[1] - pt * lng_diff), lyr))

	return point_list

def plot3D(X, Y, Z):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	# X, Y, Z = axes3d.get_test_data(0.05)
	ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

	plt.show()

if __name__ == '__main__':
	# ori = (40.69465, -73.98327)
	# dst = (40.69465, -73.98337)
	# print(geo_distance(ori, dst, 'great_circle'))

	

	plot3D([1, 3, 5, 2], [3, 6, 9, 1], [9,4,1,5])
	# point_list = hexagon((0, 0), 4, 1.1)

	# for pt in point_list:
	# 	plt.plot(pt.geo[0], pt.geo[1], 'ro')

	# plt.show()

	# print len(point_list)

