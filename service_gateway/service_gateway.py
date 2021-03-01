import uvicorn
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.openapi.utils import get_openapi
import requests

api_gateway = FastAPI(title='API Gateway',
					  description='Fetal Head Circumferences Estimator.',
					  version='1.0.0')

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


def custom_openapi():
	if api_gateway.openapi_schema:
		return api_gateway.openapi_schema
	openapi_schema = get_openapi(
		title="API Gateway",
		version="1.0.0",
		description="Fetal Head Circumferences Estimator",
		routes=api_gateway.routes,
	)
	api_gateway.openapi_schema = openapi_schema
	return api_gateway.openapi_schema


if __name__ == "__main__":
	#URL
	url = [
		"http://centerprocessing:8000/request_mask",
	]
	api_gateway.openapi = custom_openapi
	# host = 'localhost' if run local else 'servicegateway'
	uvicorn.run(api_gateway, port=8888, host='localhost', debug=True)


