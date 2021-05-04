import uvicorn
from fastapi import FastAPI, Form, File
from fastapi.openapi.utils import get_openapi
import ast
import base64
import logging
import requests
import json

global url

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

class RestServiceCenterProcessing():

	center_processing = FastAPI(title='Center Processing API',
								description='Fetal Head Circumferences Estimator.',
								version='1.0.0')

	@center_processing.post("/request_mask")
	async def insert_core(file: bytes = File(...), pixel_size: str = Form(...), filename: str = Form(...)):
		# pixel_size = float(pixel_size)
		file = base64.b64decode(file)
		""" RCNN Masker """
		headers = {}
		files = {
			'file': file
		}

		masker_response = requests.request("POST", url[0], headers=headers, files=files)
		logging.info(f"Finishing Masking process !!!")

		""" Ellipse Fitter """
		files = {
			'masked_img': masker_response.content,
			'rgb_img': file
		}

		ellipse_response = requests.request("POST", url[1], headers=headers, files=files)
		logging.info(f"Finishing Ellipse Fitting process !!!")

		ellipse_cordinates = ellipse_response.content.decode('utf-8')

		while isinstance(ellipse_cordinates, str):
			ellipse_cordinates = ast.literal_eval(ellipse_cordinates)

		""" Perimeter Estimator """
		json_ellipse_cordinates = json.dumps(ellipse_cordinates['ellipse_cordinates'])

		data = {
			'ellipse_cordinates': json_ellipse_cordinates,
			"pixel_size": pixel_size,
			"filename": filename
		}

		ellipse_perimeter = requests.request("POST", url[2], headers=headers, data=data)

		ellipse_perimeter = ellipse_perimeter.content.decode('utf-8')

		while isinstance(ellipse_perimeter, str):
			ellipse_perimeter = ast.literal_eval(ellipse_perimeter)

		# print(f"Fetal Head circumference: {ellipse_perimeter} mm")
		logging.info(f"Fetal Head circumference: {ellipse_perimeter['ellipse_perimeter']} mm")
		""" Visualize WEB API """


		""" Result """
		res = {
			"Message": "Sent successfully",
			"status": 200
		}
		return res

server = RestServiceCenterProcessing()
server = server.center_processing

def custom_openapi():
	if server.openapi_schema:
		return server.openapi_schema
	openapi_schema = get_openapi(
		title="API Ellipse Fitter",
		version="1.0.0",
		description="Fetal Head Circumferences Estimator",
		routes=server.routes,
	)
	server.openapi_schema = openapi_schema
	return server.openapi_schema


if __name__ == "__main__":
	### URL
	url = [
		'http://localhost:8200/mrcnn_masker',
		'http://localhost:8300/ellipse_fitter',
		'http://localhost:8400/perimeter_estimator'
	]

	### Fast API
	# host = 'localhost' if run local else 'center_processing'
	uvicorn.run(server, port=8100, host='localhost', debug=True)