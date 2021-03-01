import json
import ast
import logging
from fastapi import FastAPI, Form, File
import uvicorn
from splash_fit_ellipse import draw_ellipse
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from typing import List

ellipse_api = FastAPI(title='Ellipse Fitter API')

@ellipse_api.post("/ellipse_fitter")
async def ellipse_fitting(masked_img: bytes = File(...), rgb_img: bytes = File(...)):
	# Read image
	# mask = file[0]
	# rgb_img = file[1]

	masked_img = masked_img.decode("utf-8")
	# masked_img = ast.literal_eval(masked_img)
	# masked_img = ast.literal_eval(masked_img)
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
	#json_ellipse_cordinates = json.dumps(ellipse)
	json_ellipse_cordinates = json.dumps(result)

	return json_ellipse_cordinates


if __name__ == "__main__":
	# host = 'localhost' if run local else 'mrcnn_api'
	uvicorn.run(ellipse_api, port=9090, host='ellipse', debug=True)
	


