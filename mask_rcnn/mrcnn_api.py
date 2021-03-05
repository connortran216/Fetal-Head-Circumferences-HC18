import json
import ast
import logging
import uvicorn
from fastapi import FastAPI, Form, File
from PIL import Image
import numpy as np
from io import BytesIO

from splash_head import load_mrcnn_model, detect_and_color_splash

mrcnn_api = FastAPI(title='MRCNN API')

global model

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
	# json_masked_img = json.dumps(crop_mask)
	# bytes_masked_img = json_masked_img.encode('utf-8')

	return json_masked_img


if __name__ == "__main__":
	# Init Mask RCNN Model
	model = load_mrcnn_model()
	print("Finish loading Mask RCNN model !!!")

	# host = 'localhost' if run local else 'mrcnn_api'
	uvicorn.run(mrcnn_api, port=9006, host='maskrcnn', debug=True)
	


