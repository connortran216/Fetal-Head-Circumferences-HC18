"""
Mask R-CNN
Train on the toy bottle dataset and implement color splash effect.

Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Waleed Abdulla

------------------------------------------------------------

Usage: import the module (see Jupyter notebooks for examples), or run from
	   the command line as such:

	# Train a new model starting from pre-trained COCO weights
	python3 bottle.py train --dataset=/home/datascience/Workspace/maskRcnn/Mask_RCNN-master/samples/bottle/dataset --weights=coco

	# Resume training a model that you had trained earlier
	python3 bottle.py train --dataset=/path/to/bottle/dataset --weights=last

	# Train a new model starting from ImageNet weights
	python3 bottle.py train --dataset=/path/to/bottle/dataset --weights=imagenet

	# Apply color splash to an image
	python3 bottle.py splash --weights=/path/to/weights/file.h5 --image=<URL or path to file>

	# Apply color splash to video using the last weights you trained
	python3 bottle.py splash --weights=last --video=<URL or path to file>
"""
import numpy as np
import cv2
# Import Mask RCNN
from mrcnn.config import Config
from mrcnn import model as modellib

############################################################
#  Configurations
############################################################

category = 'medical'
class_names = ['BG', 'head']

class CustomConfig(Config):
	"""Configuration for training on the toy  dataset.
	Derives from the base Config class and overrides some values.
	"""
	# Give the configuration a recognizable name
	NAME = category

	# We use a GPU with 12GB memory, which can fit two images.
	# Adjust down if you use a smaller GPU.
	IMAGES_PER_GPU = 2

	# Number of classes (including background)
	NUM_CLASSES = 2  # 1 + len(class_names)  # Background + toy

	# Number of training steps per epoch
	STEPS_PER_EPOCH = 150
	VALIDATION_STEPS = 50

	# Skip detections with < 90% confidence
	DETECTION_MIN_CONFIDENCE = 0.9
	DETECTION_NMS_THRESHOLD = 0.7

	WEIGHT_DECAY = 0.0005

	# Backbone network architecture
	# Supported values are: resnet50, resnet101
	BACKBONE = "resnet101"

	IMAGE_RESIZE_MODE = "square"
	IMAGE_MIN_DIM = 540
	IMAGE_MAX_DIM = 1024

	# Length of square anchor side in pixels
	RPN_ANCHOR_SCALES = (16, 32, 64, 128, 256)

	# Non-max suppression threshold to filter RPN proposals.
	# You can increase this during training to generate more propsals.
	RPN_NMS_THRESHOLD = 0.9

	# How many anchors per image to use for RPN training
	RPN_TRAIN_ANCHORS_PER_IMAGE = 64

	# If enabled, resizes instance masks to a smaller size to reduce
	# memory load. Recommended when using high-resolution images.
	USE_MINI_MASK = True
	MINI_MASK_SHAPE = (56, 56)  # (height, width) of the mini-mask

	# Aim to allow ROI sampling to pick 33% positive ROIs.
	TRAIN_ROIS_PER_IMAGE = 400

	# Maximum number of ground truth instances to use in one image
	MAX_GT_INSTANCES = 200

	# Max number of final detections per image
	DETECTION_MAX_INSTANCES = 5


############################################################
#  Inference
############################################################


class InferenceConfig(CustomConfig):
	# Set batch size to 1 since we'll be running inference on
	# one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1


class MaskRCNN(object):
	def __init__(self):
		self.weights_path = './weights/mask_rcnn_head_final.h5'
		self.config = InferenceConfig()
		self.model = modellib.MaskRCNN(mode="inference", config=self.config, model_dir='./logs')
		self.model.load_weights(self.weights_path, by_name=True)

	def detect_and_color_splash(self, image=None):
		# rgb_img = image.copy()
		# Detect objects
		r = self.model.detect([image], verbose=1)[0]

		# Color splash
		# display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
		mask = r["masks"]

		for j in range(image.shape[2]):
			image[:, :, j] = image[:, :, j] * mask[:, :, 0]

		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		image = np.where(image > 0, 255, image)

		# Combine surrounding noise with ROI
		kernel = np.ones((6, 6), np.uint8)
		image = cv2.dilate(image, kernel, iterations=3)

		# filename = "crop_mask.jpg"
		# cv2.imwrite(filename, image)

		return image

# if __name__ == "__main__":
# 	import cv2
# 	image = cv2.imread("000_HC.png")
#
# 	model = MaskRCNN()
# 	mask = model.detect_and_color_splash(image)
