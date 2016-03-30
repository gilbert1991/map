

# Sample Location with geo-coord and the layer it in
class Point(object):
	def __init__(self, lat = None, lng = None, layer = None):
		self.lat = lat
		self.lng = lng
		self.layer = layer