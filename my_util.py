import geopy.distance as gpy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

import objects as obj
import http_handler as hh

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

def snapRoadNetwork(origin, radius, interval):
	network = []

	vertices = sliceCircle(origin, radius * 2, 8)

	for idx in range(0, 8):
		v1 = vertices[idx]
		v2 = vertices[(idx+2) % 8]
		road = hh.parseJsonRoad(hh.snapToRoad([v1, v2]))

		# for idx2 in range(len(road) - 1):
		# 	p1 = road[idx2]
		# 	p2 = road[idx2+1]

		# 	if np.sqrt((p2[1]-p1[1])**2+(p2[0]-p1[0])**2) > radius:


		# 	network.extend(subRoad)
		network.extend(road)
	return network

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
	for idx in range(size - 1):
		p1 = path[idx]
		p2 = path[idx+1]

		# interpolate if distance between consecutive points less than 2*threshold
		if np.sqrt((p2[1]-p1[1])**2+(p2[0]-p1[0])**2) > interval*2:
			path.append( ( (p2[0]+p1[0])/2, (p2[1]+p1[1])/2 ) )

	# in place sorting
	path.sort(key=lambda tup: tup[0])

	return path

# Sample Location Generation
def hexagon(origin = (0, 0), radius = 20, interval = 1):

	print 'Generating hexagon points...'
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

	print '%d points and %d layers generated' % (len(point_list), no_layer)

	return point_list

def plotMultiWeights(img_list, headings):
	size = len(headings)

	fig = plt.figure()

	cmhot = plt.get_cmap("hot")

	for i in range(size):
		heading = headings[i]

		sub_list = [img for img in img_list if img.cameraPara.heading == heading]
		geo_list = [img.location.geo for img in sub_list]
		x = [geo[0] for geo in geo_list]
		y = [geo[1] for geo in geo_list]
		z = [img.weight for img in sub_list]

		ax = fig.add_subplot(1, size, i+1, projection='3d')
		ax.scatter(x, y, z, s=50, c=np.abs(z), cmap=cmhot)
		ax.set_title('Heading %s' % heading)

	plt.show()

def plot3D(x, y, z):
	# fig = plt.figure()
	# ax = fig.add_subplot(111, projection='3d')
	# # X, Y, Z = axes3d.get_test_data(0.05)
	# ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

	# plt.show()

	fig = plt.figure()
	ax = fig.gca(projection='3d')

	cmhot = plt.get_cmap("hot")
	ax.scatter(x, y, z, s=50, c=np.abs(z), cmap=cmhot)
	# ax.scatter(x, y, z, c=z)
	plt.show()

def plotPath(path):
	x = []
	y = []
	for p in path:
		x.append(p[1])
		y.append(p[0])		

	fig, ax = plt.subplots()

	marker_style = dict(color='cornflowerblue', linestyle=':', marker='o', 
		markersize=8, markerfacecoloralt='gray')

	# Plot all fill styles
	ax.plot(x, y, fillstyle='full', **marker_style)

	plt.show()


if __name__ == '__main__':
	# path = [(-35.27801,149.12958),(-35.28032,149.12907),(-35.28099,149.12929),(-35.28144,149.12984),(-35.28194,149.13003),(-35.28282,149.12956)]
	# path = sliceCircle((0,0), 10, 8)
	# plotPath(path)
	# network = snapRoadNetwork((40.693903, -73.983434), 0.0005, 0.00005)
	# plotPath(network)
	path = [(0.0, 0.0), (3.0, 4.0)]
	path = interpolate(path, 2)
	print path



