import uvicorn
from fastapi import FastAPI, Form, UploadFile, File
import requests

api_gateway = FastAPI(title='API Gateway')

global url

@api_gateway.post("/service_gateway_upload")
async def insert(pixel_size: str = Form(...), file: UploadFile = File(...)):

	data = {
		"pixel_size": pixel_size
	}

	files = {
		'file': file.file
	}
	
	headers = {}

	insert_response = requests.request("POST", url[0], headers=headers, data=data, files=files)

	#return json_insert
	res = {
		"Message": 'Sent successfully !!!',
		"status": 200
	}

	return res


if __name__ == "__main__":
	#URL
	url = [
		"http://centerprocessing:8000/request_mask",
	]

	# host = 'localhost' if run local else 'servicegateway'
	uvicorn.run(api_gateway, port=8888, host='servicegateway', debug=True)