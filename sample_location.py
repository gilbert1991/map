import math
import matplotlib.pyplot as plt

# Sample Location with geo-coord and the layer it in
class Point(object):
	def __init__(self, lat = None, lng = None, layer = None):
		self.lat = lat
		self.lng = lng
		self.layer = layer

# Sample Location Generation
def hexagon(origin = (0, 0), radius = 20, interval = 1):
	# init point list with origin at layer 0
	point_list = [Point(origin[0], origin[1], layer = 0)] 

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
		layer_list.append(Point(origin[0] + unit_length, origin[1], lyr))  
		layer_list.append(Point(origin[0] + unit_length / 2, origin[1] + height_length, lyr)) 
		layer_list.append(Point(origin[0] - unit_length / 2, origin[1] + height_length, lyr))
		layer_list.append(Point(origin[0] - unit_length, origin[1], lyr))  
		layer_list.append(Point(origin[0] - unit_length / 2, origin[1] - height_length, lyr))  
		layer_list.append(Point(origin[0] + unit_length / 2, origin[1] - height_length, lyr))

		# number of points on an edge exclude two vertices
		no_point_on_edge = lyr - 1 

		# Append start vertext and points on edge , edge by edge
		for edge in range(6):
			v_start = layer_list[edge]
			v_end = layer_list[(edge + 1) % 6]

			lat_diff = (v_start.lat - v_end.lat) / (no_point_on_edge + 1)
			lng_diff = (v_start.lng - v_end.lng) / (no_point_on_edge + 1)

 			point_list.append(v_start)

			for pt in range(1, no_point_on_edge + 1):
				point_list.append(Point(v_start.lat - pt * lat_diff, v_start.lng - pt * lng_diff, lyr))

	return point_list


if __name__ == '__main__':
	point_list = hexagon((0, 0), 4, 1.1)

	# for pt in point_list:
	# 	plt.plot(pt.lat, pt.lng, 'ro')

	# plt.show()

	print len(point_list)



