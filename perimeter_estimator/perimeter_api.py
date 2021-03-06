import json
import ast
import logging
from fastapi import FastAPI, Form, File
from fastapi.openapi.utils import get_openapi
import uvicorn
from ellipse_perimeter import Perimeter


class RestServicePerimeterEstimator():
	perimeter_estimator = FastAPI(title='Perimeter Estimator API',
								  description='Fetal Head Circumferences Estimator.',
								  version='1.0.0')

	@staticmethod
	@perimeter_estimator.post("/perimeter_estimator")
	async def perimeter_estimating(ellipse_cordinates: str = Form(...), pixel_size: str = Form(...), filename: str = Form(...)):

		ellipse_cordinates = ast.literal_eval(ellipse_cordinates)
		pixel_size = float(pixel_size)

		ellipse_perimeter = Perimeter(ellipse_cordinates, pixel_size, filename)

		result = {
			"ellipse_perimeter": ellipse_perimeter
		}
		# Compress data
		json_ellipse_perimeter = json.dumps(result)

		return json_ellipse_perimeter


def custom_openapi():
	if server.openapi_schema:
		return server.openapi_schema
	openapi_schema = get_openapi(
		title="API Perimeter",
		version="1.0.0",
		description="Fetal Head Circumferences Estimator",
		routes=server.routes,
	)
	server.openapi_schema = openapi_schema
	return server.openapi_schema


if __name__ == "__main__":
	server = RestServicePerimeterEstimator()
	server = server.perimeter_estimator
	server.openapi = custom_openapi

	# host = 'localhost' if run local else 'perimeter'
	uvicorn.run(server, port=8400, host='localhost', debug=True)