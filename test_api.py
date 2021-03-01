import requests
import threading
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def send_request():
	url = [
		"http://localhost:8888/service_gateway_upload"
	]

	df = pd.read_csv("test_set_pixel_size.csv", delimiter=";")
	sample_data = df.sample()

	filename = sample_data["filename"].values[0]
	pixel_size = sample_data["pixel size(mm)"].values[0]

	filename = "test_set/" + str(filename)
	# pixel_size = 0.0691358041432
	# filename = "000_HC.png"
	print("File name: ", filename)

	with open(filename, 'rb') as image_file:
		#img_1 = image_file.read()
		img_1 = base64.b64encode(image_file.read())

	headers = {}

	data = {
		"pixel_size": str(pixel_size)
	}

	files = {
		'file': img_1
	}

	### insert
	result = requests.post(url[0], headers=headers, data=data, files=files)
	print("Result: ", result)



if __name__ == "__main__":
	# creating thread
	#t1 = threading.Thread(target=request_get_img, args=())
	t1 = threading.Thread(target=send_request, args=())
	# starting thread 1
	t1.start()

	# wait until thread 1 is completely executed
	t1.join()

	# both threads completely executed
	print("Done!")

