# Python3 program to find perimeter
# of an Ellipse
from math import sqrt
import numpy as np
# ((410.1819763183594, 374.40362548828125), (211.892822265625, 244.91175842285156), 39.05967712402344)

# Function to find the perimeter
# of an Ellipse
def Perimeter(ellipse_cordinates, pixel_size):
    # factor = row["pixel size(mm)"]
    (xx, yy), (MA, ma), angle = ellipse_cordinates

    center_x_mm = yy #factor * yy
    center_y_mm = xx #factor * xx
    semi_axes_a_mm = ma / 2 #factor * ma / 2
    semi_axes_b_mm = MA / 2 #factor * MA / 2
    angle_rad = (-angle * np.pi / 180) % np.pi
    # print(center_x_mm, center_y_mm, semi_axes_a_mm, semi_axes_b_mm, angle_rad)


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

