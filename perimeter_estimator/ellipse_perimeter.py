import numpy as np

__all__ = ['Perimeter']


# Function to find the perimeter of an Ellipse
def Perimeter(ellipse_cordinates, pixel_size):
	(xx, yy), (MA, ma), angle = ellipse_cordinates

	center_x_mm = pixel_size * yy
	center_y_mm = pixel_size * xx
	semi_axes_a_mm = pixel_size * ma / 2
	semi_axes_b_mm = pixel_size * MA / 2
	angle_rad = (-angle * np.pi / 180) % np.pi

	h = (semi_axes_a_mm - semi_axes_b_mm) ** 2 / (semi_axes_a_mm + semi_axes_b_mm) ** 2

	circ = (
			np.pi
			* (semi_axes_a_mm + semi_axes_b_mm)
			* (1 + (3 * h) / (10 + np.sqrt(4 - 3 * h)))
	)

	return circ

# ellipse_cordinates = ((410.1819763183594, 374.40362548828125), (211.892822265625, 244.91175842285156), 39.05967712402344)
# Perimeter(ellipse_cordinates)


def hc18_result(ellipse_cordinates, pixel_size, filename):
	(xx, yy), (MA, ma), angle = ellipse_cordinates

	center_x_mm = pixel_size * yy
	center_y_mm = pixel_size * xx

	semi_axes_a_mm = pixel_size * ma / 2
	semi_axes_b_mm = pixel_size * MA / 2

	angle_rad = (-angle * np.pi / 180) % np.pi
	# print(center_x_mm, center_y_mm, semi_axes_a_mm, semi_axes_b_mm, angle_rad)

	h = (semi_axes_a_mm - semi_axes_b_mm) ** 2 / (semi_axes_a_mm + semi_axes_b_mm) ** 2

	circ = (
			np.pi
			* (semi_axes_a_mm + semi_axes_b_mm)
			* (1 + (3 * h) / (10 + np.sqrt(4 - 3 * h)))
	)
	data = filename, center_x_mm, center_y_mm, semi_axes_a_mm, semi_axes_b_mm, angle_rad
	with open('result.txt', 'a') as file:
		file.write(','.join(map(repr, data)) + "\n")

	# print("circ: ", circ*0.06913580414319999)

	return circ