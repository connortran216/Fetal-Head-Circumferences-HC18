import numpy as np

import cv2


def opencv_fitEllipse(img, method="Direct"):
    #assert binary_mask.min() >= 0.0 and binary_mask.max() <= 1.0
    # points = np.argwhere(binary_mask == 1)  # TODO: tune threshold

    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # c_img = cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    # plt.figure()
    # plt.imshow(c_img)
    # plt.show()

    for c in contours:
        ellipse = cv2.fitEllipse(c)

    if method == "AMS":
        for c in contours:
            ellipse = cv2.fitEllipseAMS(c)
    elif method == "Direct":
        for c in contours:
            ellipse = cv2.fitEllipseDirect(c)
    elif method == "Simple":
        for c in contours:
            ellipse = cv2.fitEllipse(c)
    else:
        raise ValueError("Wrong method")

    return ellipse



import matplotlib.pyplot as plt

def draw_ellipse(img, rgb_img):


    ellipse = opencv_fitEllipse(img)

    # (xx, yy), (MA, ma), angle = opencv_fitEllipse(img)
    #
    # print(ellipse)

    cv2.ellipse(
        rgb_img,
        ellipse,
        color=(255, 0, 0),
        thickness=3,
    )

    # filename = "ellipse_on_crop_mask.jpg"
    # cv2.imwrite(filename, rgb_img)
    # plt.imshow(rgb_img)
    # plt.show()

    # ####
    # cv2.ellipse(
    #     img,
    #     ellipse,
    #     color=(255, 0, 0),
    #     thickness=3,
    # )
    # contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    #
    # perimeter = cv2.arcLength(contours, True)
    # print("Perimeter: ", perimeter)

    # c_img = cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    # plt.figure()
    # plt.imshow(c_img)
    # plt.show()

    return ellipse

