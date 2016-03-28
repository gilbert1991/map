import shutil

# Save valid image as file
def img2file(response, file_path):
	with open(file_path, 'wb') as f:
		response.raw.decode_content = True
		shutil.copyfileobj(response.raw, f)