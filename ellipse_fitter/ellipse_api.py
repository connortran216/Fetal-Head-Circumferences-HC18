import json
import ast
import base64
import cv2
import numpy as np
import uvicorn
import logging

from fastapi import FastAPI, Form, File
from fastapi.openapi.utils import get_openapi
from splash_fit_ellipse import draw_ellipse
from PIL import Image
from io import BytesIO
from basemodel.schemas import EllipseItem


class RestServiceEllipseFitter():
	ellipse_api = FastAPI(title='Ellipse Fitter API',
						  description='Fetal Head Circumferences Estimator.',
						  version='1.0.0')

	@staticmethod
	@ellipse_api.post("/ellipse_fitter")
	async def ellipse_fitting(item: EllipseItem): #masked_img: bytes = File(...), rgb_img: bytes = File(...)
		# Read image
		# masked_img = masked_img.decode("utf-8")
		masked_img = base64.b64decode(item.masked_img).decode("utf-8")
		rgb_img = base64.b64decode(item.rgb_img)

		while isinstance(masked_img, str):
			masked_img = ast.literal_eval(masked_img)

		masked_img = np.array(masked_img['crop_mask']).astype(np.uint8)

		rgb_img = Image.open(BytesIO(rgb_img)).convert('RGB')
		rgb_img = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR)

		# Extract faces and features from it
		ellipse = draw_ellipse(masked_img, rgb_img)

		result = {
			"ellipse_coordinates": ellipse,
			"ellipse_img": rgb_img.tolist()
		}
		# # Compress data
		json_ellipse_coordinates = json.dumps(result)

		return json_ellipse_coordinates


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
	server = RestServiceEllipseFitter()
	server = server.ellipse_api
	server.openapi = custom_openapi

	# host = 'localhost' if run local else 'ellipse'
	uvicorn.run(server, port=8300, host='localhost', debug=True)
	


