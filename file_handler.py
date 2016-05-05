import shutil
import os
import pickle
import ntpath as nt
import numpy as np
import cv2

import setting as st
import objects as obj

# Save valid image as file
def img2File(response, file_path):
	with open(file_path, 'wb') as f:
		response.raw.decode_content = True
		shutil.copyfileobj(response.raw, f)
		print '%s downloaded' % path_leaf(file_path)

# Get a list of files with file_ext in data_path
def listFiles(data_path, file_ext):
	f_list = []

	for f in os.listdir(data_path):
		if f.endswith(file_ext):
			f_list.append(data_path + f)

	return f_list

# Delete all *.ext files in a directory
def cleanDir(data_path, file_ext):
	f_list = listFiles(data_path, file_ext)
	for f in f_list:
		os.remove(f)

# Write items in a list to file
def writeList(my_list, file_path):
	with open(file_path, 'wb') as f:
		pickle.dump(my_list, f)
		print "List written in %s" % file_path

# Read list stored in a file
def readList(file_path):
	with open(file_path, 'rb') as f:
		my_list = pickle.load(f)

	print "List read from %s" % file_path

	return my_list

# Extract file name from file path
def path_leaf(path):
    head, tail = nt.split(path)

    return tail or nt.basename(head)

# Extract a list of image paras from a directory
def extractImageParas(file_path, file_ext, noParas):
	image_list = []

	f_list = listFiles(file_path, file_ext or '.jpeg')

	# Extract file parameters one by one
	for f in f_list:
		file_name = path_leaf(f)
		# Split file name with default "_" to get a list of parameters		
		p = os.path.splitext(file_name)[0].split('_') # get paras from file name

		# All file names should contain parameters in the same format
		if len(p) == noParas:
			p = map(float, p)
			image = obj.Image(position=[p[0], p[1]], cameraPara=obj.CameraPara(size = (p[2], p[3]), fov = p[4], heading = p[5], pitch = p[6]), filePath = f)
			image_list.append(image)
		else:
			print "Extract image parameters from %s failed" % file_name

	return image_list

def showImage(file_path):
	img = cv2.imread('/Users/Gilbert/Documents/Libraries/python/OpenSfM/data/lund/images/001.jpg')
	cv2.imshow('query', img)
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	cleanDir("/Users/Gilbert/Documents/NYU/Master_Thesis/3D_Street_Navigator/image/dataset/", ".jpeg")
