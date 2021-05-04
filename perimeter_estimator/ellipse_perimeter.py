# Python3 program to find perimeter
# of an Ellipse
from math import sqrt
import numpy as np
import pandas as pd
# ((410.1819763183594, 374.40362548828125), (211.892822265625, 244.91175842285156), 39.05967712402344)

# Function to find the perimeter
# of an Ellipse
def Perimeter(ellipse_cordinates, pixel_size, filename):
	# factor = row["pixel size(mm)"]

	(xx, yy), (MA, ma), angle = ellipse_cordinates

	factor = pixel_size
	center_x_mm = factor*xx #factor * yy
	center_y_mm = factor*yy #factor * xx
	semi_axes_a_mm = factor*ma / 2 #factor * ma / 2
	semi_axes_b_mm = factor*MA / 2 #factor * MA / 2
	angle_rad = (-angle * np.pi / 180) % np.pi
	# print(center_x_mm, center_y_mm, semi_axes_a_mm, semi_axes_b_mm, angle_rad)

	data = filename, center_x_mm, center_y_mm, semi_axes_a_mm, semi_axes_b_mm, angle_rad
	with open("result.txt", "a") as file:
		file.write(','.join(map(repr, data)) + "\n")

	h = (semi_axes_a_mm - semi_axes_b_mm) ** 2 / (
			semi_axes_a_mm + semi_axes_b_mm
	) ** 2
	circ = (
			np.pi
			* (semi_axes_a_mm + semi_axes_b_mm)
			* (1 + (3 * h) / (10 + np.sqrt(4 - 3 * h)))
	)

	# print("circ: ", circ*0.06913580414319999)

	return circ*pixel_size

# ellipse_cordinates = ((410.1819763183594, 374.40362548828125), (211.892822265625, 244.91175842285156), 39.05967712402344)
# Perimeter(ellipse_cordinates)

