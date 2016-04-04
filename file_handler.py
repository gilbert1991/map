import shutil
import os

# Save valid image as file
def img2File(response, file_path):
	with open(file_path, 'wb') as f:
		response.raw.decode_content = True
		shutil.copyfileobj(response.raw, f)

def listFiles(data_path, file_ext):
	f_list = []

	for f in os.listdir(data_path):
		if f.endswith(file_ext):
			f_list.append(f)

	return f_list


if __name__ == '__main__':
	listFiles()