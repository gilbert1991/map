import objects as obj
import my_util as mt
import math

# initial parameters for segmentation
sectors = 8 # number of sectors in the circle (12 means 30 degrees per sector)
radius = 90.0 # circle radius
start = 0 # start of circle in degrees
end = 360 # end of circle in degrees
center = obj.Location(geo=(0,0))

# prepare parameters
if start > end:
    start = start - 360
else:
    pass

sector_width = (end-start) / sectors

# helper function to calculate point from relative polar coordinates (degrees)
def polar_point(origin_point, angle,  distance):
    return [origin_point.geo[0] + math.sin(math.radians(angle)) * distance, origin_point.geo[1] + math.cos(math.radians(angle)) * distance]

segment_vertices = []

for x in xrange(0, sectors):
    segment_vertices.append(polar_point(center, start + x*sector_width,radius))

print segment_vertices
mt.plotPath(segment_vertices)