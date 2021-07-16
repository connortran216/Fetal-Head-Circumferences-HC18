from pydantic import BaseModel
from typing import List


class CenterItem(BaseModel):
	pixel_size: str
	filename: str
	file: str


class EllipseItem(BaseModel):
	masked_img: str
	rgb_img: str


class PerimeterItem(CenterItem):
	ellipse_coordinates: str
