import json
import ast
import logging
from fastapi import FastAPI, Form, File
import uvicorn
from ellipse_perimeter import Perimeter

perimeter_estimator = FastAPI(title='Perimeter Estimator API')



@perimeter_estimator.post("/perimeter_estimator")
async def perimeter_estimating(ellipse_cordinates: str = Form(...), pixel_size: str = Form(...)):

    ellipse_cordinates = ast.literal_eval(ellipse_cordinates)
    pixel_size = float(pixel_size)

    ellipse_perimeter = Perimeter(ellipse_cordinates, pixel_size)

    result = {
        "ellipse_perimeter": ellipse_perimeter
    }
    # # Compress data
    json_ellipse_perimeter = json.dumps(result)

    return json_ellipse_perimeter


if __name__ == "__main__":
    # host = 'localhost' if run local else 'mrcnn_api'
    uvicorn.run(perimeter_estimator, port=9009, host='perimeter', debug=True)



