import uvicorn
import ast
import base64
import logging
import requests
import json

from fastapi import FastAPI, Form, File
from fastapi.openapi.utils import get_openapi
from basemodel.schemas import CenterItem


global url

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class RestServiceCenterProcessing:
	center_processing = FastAPI(title='Center Processing API',
								description='Fetal Head Circumferences Estimator.',
								version='1.0.0')

	@staticmethod
	def response_decode(response):
		content = response.content.decode('utf-8')

		while isinstance(content, str):
			content = ast.literal_eval(content)

		return content

	@staticmethod
	@center_processing.post("/request_mask")
	async def insert_core(item: CenterItem):

		# file = base64.b64decode(file)

		"""
			RCNN Masker
		"""

		headers = {}
		files = {
			'file': base64.b64decode(item.file)
		}

		masker_response = requests.request("POST", url[0], files=files)
		logging.info(f"Finishing Masking process !!!")

		""" 
			Ellipse Fitter 
		"""

		data = {
			'masked_img': base64.b64encode(masker_response.content).decode("utf-8"),
			'rgb_img': item.file
		}

		ellipse_response = requests.request("POST", url[1], json=data)
		logging.info(f"Finishing Ellipse Fitting process !!!")

		ellipse_coordinates = RestServiceCenterProcessing.response_decode(ellipse_response)

		""" 
			Perimeter Estimator 
		"""
		json_ellipse_coordinates = json.dumps(ellipse_coordinates['ellipse_coordinates'])

		data = {
			'ellipse_coordinates': json_ellipse_coordinates,
			"pixel_size": item.pixel_size,
			"filename": item.filename,
			"file": "abc"
		}

		ellipse_perimeter = requests.request("POST", url[2], headers=headers, json=data)

		ellipse_perimeter = RestServiceCenterProcessing.response_decode(ellipse_perimeter)
		logging.info(f"Fetal Head circumference: {ellipse_perimeter['ellipse_perimeter']} mm")

		""" 
			Visualize WEB API 
		"""
		""" 
			Result 
		"""
		res = {
			"Message": "Sent successfully",
			"status": 200
		}
		return res


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

	server = RestServiceCenterProcessing()
	server = server.center_processing
	server.openapi = custom_openapi

	### Fast API
	# host = 'localhost' if run local else 'center_processing'
	uvicorn.run(server, port=8100, host='localhost', debug=True)