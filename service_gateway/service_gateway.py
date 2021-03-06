import uvicorn
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.openapi.utils import get_openapi
import requests


global url

class RestServiceGateway:
	api_gateway = FastAPI(title='API Gateway',
						  description='Fetal Head Circumferences Estimator.',
						  version='1.0.0')

	@staticmethod
	@api_gateway.post("/service_gateway_upload")
	async def insert(pixel_size: str = Form(...), filename: str = Form(...), file: UploadFile = File(...)):

		data = {
			"pixel_size": pixel_size,
			"filename": filename
		}

		files = {
			'file': file.file
		}

		insert_response = requests.request("POST", url[0], data=data, files=files)

		#return json_insert
		res = {
			"Message": 'Upload successfully !!!',
			"status": 200
		}

		return res


def custom_openapi():
	if server.openapi_schema:
		return server.openapi_schema
	openapi_schema = get_openapi(
		title="API Gateway",
		version="1.0.0",
		description="Fetal Head Circumferences Estimator",
		routes=server.routes,
	)
	server.openapi_schema = openapi_schema
	return server.openapi_schema


if __name__ == "__main__":
	#URL
	url = [
		"http://localhost:8100/request_mask",
	]

	server = RestServiceGateway()
	server = server.api_gateway
	server.openapi = custom_openapi

	# host = 'localhost' if run local else 'servicegateway'
	uvicorn.run(server, port=8888, host='localhost', debug=True)


