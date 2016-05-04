import geopy.distance as gpy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

import objects as obj
import http_handler as hh

def snapRoadNetwork(origin, radius, interval):
	print 'Snap road networks at (%f, %f) with radius %f' % (origin[0], origin[1], radius)
	network = []

	# Slice a circle into 8 sectors with 2*radius
	sector = 8
	vertices = sliceCircle(origin, radius * 2, sector)

	# Create virtual paths for road snapping
	for idx in range(0, sector):
		v1 = vertices[idx]
		v2 = vertices[(idx+2) % sector]

		path = [v1, v2]

		# snap path to road 
		road = hh.parseJsonRoad(hh.snapToRoad(path))
		# interpolate the road and snap again to get optimized sample locations
		road = hh.parseJsonRoad(hh.snapToRoad(interpolate(road, interval)))		
		filterPath(road, interval)		
		
		#reverse the query to better cover the area
		reverse_road = hh.parseJsonRoad(hh.snapToRoad(list(reversed(road)))) if road else []		
		reverse_road = hh.parseJsonRoad(hh.snapToRoad(interpolate(reverse_road, interval)))
		filterPath(reverse_road, interval)
		
		# Exclude points beyond radius
		road = [pt for pt in road if np.sqrt((pt[1]-origin[1])**2+(pt[0]-origin[0])**2) < radius]
		reverse_road = [pt for pt in reverse_road if np.sqrt((pt[1]-origin[1])**2+(pt[0]-origin[0])**2) < radius]

		# Add path to sample network
		network.append(road)
		network.append(reverse_road)

	# places = [pt for road in network for pt in road]
	# for idx in list(reversed(range(len(places)))):
	# 	for idx2 in list(reversed(range(len(places), idx+1))):
	# 		if np.sqrt((places[idx][1]-places[idx2][1])**2+(places[idx][0]-places[idx2][0])**2) < interval:
	# 			del places[idx2]

	# network = places
	# network.append([])

	return network

def filterPath(path, interval):
	# Filter the samples with density 1/interval
	for i in list(reversed(range(len(path)))):
		if np.sqrt((path[i-1][1]-path[i][1])**2+(path[i-1][0]-path[i][0])**2) < interval:
			del path[i-1]

	return path

# Evenly slice a circle into sectors
def sliceCircle(origin, radius, sectors):
	sector_width = 360 / sectors

	vertices = []

	for x in range(0, sectors):
		vertex = (origin[0] + np.sin(np.radians(x * sector_width)) * radius, 
					origin[1] + np.cos(np.radians(x * sector_width)) * radius)
		vertices.append(vertex)

	return vertices

# interpolate points if the interval is too large
def interpolate(path, interval):
	size = len(path)
	result_path = []

	for idx in range(size - 1):
		p1 = path[idx]
		p2 = path[idx+1]

		result_path.append(p1)

		# number of interpolating points needed
		interpolate_points = np.floor( np.sqrt((p2[1]-p1[1])**2+(p2[0]-p1[0])**2) / interval ) - 1

		if interpolate_points > 0:
			# calculate the steps of lat & lng
			step0 = (p2[0]-p1[0]) / (interpolate_points + 1)
			step1 = (p2[1]-p1[1]) / (interpolate_points + 1)

			# insert the inter points
			for idx in range(1, int(interpolate_points+1)):
				result_path.append((p1[0]+idx*step0, p1[1]+idx*step1))

		result_path.append(p2)

	return result_path

def plotMultiWeights(img_list, headings, maxWeight):
	size = len(headings)

	fig = plt.figure()

	cmhot = plt.get_cmap("hot")

	print maxWeight
	for i in range(size):
		heading = headings[i]

		sub_list = [img for img in img_list if img.cameraPara.heading == heading]
		geo_list = [img.location.geo for img in sub_list]
		x = [geo[0] for geo in geo_list]
		y = [geo[1] for geo in geo_list]
		z = [img.weight for img in sub_list]

		ax = fig.add_subplot(1, size, i+1, projection='3d')
		ax.scatter(x, y, z, s=50, c=np.abs(z), cmap=cmhot)
		ax.set_zlim([0, float( maxWeight)])
		ax.set_title('Heading %s' % heading)

	plt.show()

def plot3D(x, y, z):
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	cmhot = plt.get_cmap("hot")
	ax.scatter(x, y, z, s=50, c=np.abs(z), cmap=cmhot)

	plt.show()

def plotNetwork(network):
	marker_style = dict(color='cornflowerblue', linestyle=':', marker='o', 
			markersize=8, markerfacecoloralt='gray')

	fig, ax = plt.subplots()

	for path in network:
		x = []
		y = []
		for p in path:
			x.append(p[1])
			y.append(p[0])		

		# Plot all fill styles
		ax.plot(x, y, fillstyle='full', **marker_style)

	plt.show()


if __name__ == '__main__':
	network = snapRoadNetwork((40.693903, -73.983434), 0.0005, 0.0001)
	print '%d locations sampled in network' % sum([len(path) for path in network])
	plotNetwork(network)


	# path = [(40.693902999999999, -73.982433999999998), (40.694902999999996, -73.983434000000003)]
	# # path = interpolate([v1, v2], interval)
	# road = hh.parseJsonRoad(hh.snapToRoad(path))
	# print road
	# print interpolate(road, 0.0001)


# /Depricated
# Convert geo coords (lat, lng) diff to distance in meters
# lat: 0.0001 ~= 11.1m, lng 0.0001 ~= 8.5m
# def geoDistance(ori, dst, method='vincenty'):
# 	if method == 'vincenty':
# 		distance = gpy.vincenty(ori, dst).meters
# 	elif method == 'great_circle':
# 		distance = gpy.great_circle(ori, dst).meters
# 	else:
# 		print('Error with geo_distance')

# 	return distance	


# /Depricated
# Sample Location Generation 
# def hexagon(origin = (0, 0), radius = 20, interval = 1):

# 	print 'Generating hexagon points...'
# 	# init point list with origin at layer 0
# 	point_list = [(origin[0], origin[1])]

# 	# number of layers to cover the area
# 	# layer is the position of a hexagon
# 	no_layer = int(math.ceil(radius / interval)) 

# 	# Generate points layer by layer 
# 	for lyr in range(1, no_layer + 1):
# 		unit_length = interval * lyr
# 		height_length = unit_length * math.sqrt(3) / 2

# 		layer_list = []

# 		# Create 6 vertices
# 		#   3 o---o 2
# 		#    / \ / \
# 		# 4 o---o---o 1
# 		#    \ / \ /
# 		#   5 o---o 6
# 		layer_list.append((origin[0] + unit_length, origin[1])) # 1
# 		layer_list.append((origin[0] + unit_length / 2, origin[1] + height_length)) # 2
# 		layer_list.append((origin[0] - unit_length / 2, origin[1] + height_length)) # 3
# 		layer_list.append((origin[0] - unit_length, origin[1])) # 4
# 		layer_list.append((origin[0] - unit_length / 2, origin[1] - height_length)) # 5 
# 		layer_list.append((origin[0] + unit_length / 2, origin[1] - height_length)) # 6

# 		# number of points on an edge exclude two vertices
# 		no_point_on_edge = lyr - 1 

# 		# Append start vertext and points on edge , edge by edge
# 		for edge in range(6):
# 			v_start = layer_list[edge]
# 			v_end = layer_list[(edge + 1) % 6]

# 			lat_diff = (v_start[0] - v_end[0]) / (no_point_on_edge + 1)
# 			lng_diff = (v_start[1] - v_end[1]) / (no_point_on_edge + 1)

#  			point_list.append(v_start)

# 			for pt in range(1, no_point_on_edge + 1):
# 				point_list.append((v_start[0] - pt * lat_diff, v_start[1] - pt * lng_diff))

# 	print '%d points and %d layers generated' % (len(point_list), no_layer)

# 	return point_list



