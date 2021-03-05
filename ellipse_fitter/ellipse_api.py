import json
import ast
import logging
from fastapi import FastAPI, Form, File
from fastapi.openapi.utils import get_openapi
import uvicorn
from splash_fit_ellipse import draw_ellipse
from PIL import Image
from io import BytesIO
import cv2
import numpy as np


class RestServiceEllipseFitter():
	ellipse_api = FastAPI(title='Ellipse Fitter API',
						  description='Fetal Head Circumferences Estimator.',
						  version='1.0.0')

	@ellipse_api.post("/ellipse_fitter")
	async def ellipse_fitting(masked_img: bytes = File(...), rgb_img: bytes = File(...)):
		# Read image
		masked_img = masked_img.decode("utf-8")

		while isinstance(masked_img, str):
			masked_img = ast.literal_eval(masked_img)

		masked_img = np.array(masked_img['crop_mask']).astype(np.uint8)


		rgb_img = Image.open(BytesIO(rgb_img)).convert('RGB')
		rgb_img = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR)

		# Extract faces and features from it
		ellipse, rgb_img = draw_ellipse(masked_img, rgb_img)

		result = {
			"ellipse_cordinates": ellipse,
			"ellipse_img": rgb_img.tolist()
		}
		# # Compress data
		json_ellipse_cordinates = json.dumps(result)

		return json_ellipse_cordinates

server = RestServiceEllipseFitter()
server = server.ellipse_api

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
	# host = 'localhost' if run local else 'mrcnn_api'
	uvicorn.run(server, port=9090, host='mrcnn_api', debug=True)
	


