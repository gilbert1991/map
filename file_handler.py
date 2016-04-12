import shutil
import os
import pickle
import ntpath as nt
import numpy as np

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
def extractImageParas(file_path, file_ext):
	image_list = []

	f_list = listFiles(file_path, file_ext or '.jpeg')

	for f in f_list:
		file_name = path_leaf(f)
		p = os.path.splitext(file_name)[0].split('_') # get paras from file name

		if len(p) == 8:
			p = map(float, p)
			image = obj.Image(obj.Location([p[0], p[1]], p[2]), obj.CameraPara(size = (p[3], p[4]), fov = p[5], heading = p[6], pitch = p[7]), filePath = f)
			image_list.append(image)
		else:
			print "Extract image parameters from %s failed" % file_name

	return image_list


if __name__ == '__main__':
	img_list =  extractImageParas(st.path + "image/dataset/", ".jpeg")
