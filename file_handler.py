import shutil
import os
import pickle
import ntpath as nt
import numpy as np

import setting as st

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

# Store list of objects.Image into file
# def writeImages(images, file_path):
# 	images = []

# Read list of Images stored in a file
# def readImages(file_path):
# 	images = []

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

def path_leaf(path):
    head, tail = nt.split(path)

    return tail or nt.basename(head)

if __name__ == '__main__':
	votes = readList(st.path + "vote.txt")
	print (len(votes), np.max(votes), np.min(votes))
