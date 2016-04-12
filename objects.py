# Image object
class Image(object):
	"""Image Object with location and other parameters"""
	def __init__(self, location = None, cameraPara = None, filePath = None, feature = None, weight = None):
		super(Image, self).__init__()
		self.location = location
		self.cameraPara = cameraPara
		self.filePath = filePath
		self.feature = feature
		self.weight = weight

# Sample Location with geo-coord and the layer it in
class Location(object):
	def __init__(self, geo = None, layer = None):
		self.geo = geo
		self.layer = layer

class CameraPara(object):
	"""docstring for CameraPara"""
	def __init__(self, size = None, fov = None, heading = None, pitch = None):
		super(CameraPara, self).__init__()
		self.size = size
		self.fov = fov
		self.heading = heading
		self.pitch = pitch
		