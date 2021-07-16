import json
import ast
import logging
import uvicorn
from fastapi import FastAPI, Form, File
from fastapi.openapi.utils import get_openapi
from PIL import Image
import numpy as np
from io import BytesIO
import cv2
# from splash_head import load_mrcnn_model, detect_and_color_splash
from MaskRCNN import MaskRCNN

global model


class RestServiceMRCNN():
	mrcnn_api = FastAPI(title='MRCNN API',
						description='Fetal Head Circumferences Estimator.',
						version='1.0.0')

	@staticmethod
	@mrcnn_api.post("/mrcnn_masker")
	async def mask_api(file: bytes = File(...)):
		# Read image
		image = Image.open(BytesIO(file)).convert('RGB')
		image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

		crop_mask = model.detect_and_color_splash(image=image)

		filename = "crop_mask.jpg"
		cv2.imwrite(filename, image)

		# Compress data
		crop_mask = crop_mask.tolist()
		result = {
			"crop_mask": crop_mask
		}
		json_masked_img = json.dumps(result)

		return json_masked_img


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
	# Init Mask RCNN Model
	# model = load_mrcnn_model()
	model = MaskRCNN()
	print("Finish loading Mask RCNN model !!!")

	server = RestServiceMRCNN()
	server = server.mrcnn_api
	server.openapi = custom_openapi

	# host = 'localhost' if run local else 'maskrcnn'
	uvicorn.run(server, port=8200, host='localhost', debug=True)
	


