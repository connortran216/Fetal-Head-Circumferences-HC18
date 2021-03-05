import json
import ast
import logging
import uvicorn
from fastapi import FastAPI, Form, File
from fastapi.openapi.utils import get_openapi
from PIL import Image
import numpy as np
from io import BytesIO

from splash_head import load_mrcnn_model, detect_and_color_splash

global model

class RestServiceMRCNN:
	mrcnn_api = FastAPI(title='MRCNN API',
						description='Fetal Head Circumferences Estimator.',
						version='1.0.0')

	@mrcnn_api.post("/mrcnn_masker")
	async def mask_api(file: bytes = File(...)):
		# Read image
		import cv2
		image = Image.open(BytesIO(file)).convert('RGB')
		image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

		crop_mask, rgb_img = detect_and_color_splash(model, image=image)

		# Compress data
		crop_mask = crop_mask.tolist()
		result = {
			"crop_mask": crop_mask
		}
		json_masked_img = json.dumps(result)

		return json_masked_img

server = RestServiceMRCNN()
server = server.mrcnn_api

def custom_openapi():
	if server.openapi_schema:
		return server.openapi_schema
	openapi_schema = get_openapi(
		title="API MRCNN",
		version="1.0.0",
		description="Fetal Head Circumferences Estimator",
		routes=server.routes,
	)
	server.openapi_schema = openapi_schema
	return server.openapi_schema


if __name__ == "__main__":
	# Init Mask RCNN Model
	model = load_mrcnn_model()
	print("Finish loading Mask RCNN model !!!")

	# host = 'localhost' if run local else 'mrcnn_api'
	uvicorn.run(server, port=9006, host='mrcnn_api', debug=True)
	


