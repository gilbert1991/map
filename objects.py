# Image object
class Image(object):
	"""Image Object with location and other parameters
	position = (lat, lng, alt)

	"""
	def __init__(self, position, filePath, rotation=None, cameraPara = None, feature = None, weight = None):
		super(Image, self).__init__()
		self.position = position
		self.cameraPara = cameraPara
		self.filePath = filePath
		self.feature = feature
		self.weight = weight
		self.rotation = rotation

class CameraPara(object):
	"""docstring for CameraPara"""
	def __init__(self, size = None, fov = None, heading = None, pitch = None):
		super(CameraPara, self).__init__()
		self.size = size
		self.fov = fov
		self.heading = heading
		self.pitch = pitch
		