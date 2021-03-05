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
# import libs
import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
import cv2
from mrcnn.visualize import display_instances
import matplotlib.pyplot as plt
from pycocotools.coco import COCO
import skimage.io as io
import pylab
import random
from tqdm import tqdm
import time

from imgaug import augmenters as iaa
from mrcnn import visualize

# Root directory of the project
ROOT_DIR = os.path.abspath("./")

# Import Mask RCNN
from mrcnn.config import Config
from mrcnn import model as modellib, utils

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join('./weights', "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")

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
#  Dataset
############################################################

class CustomDataset(utils.Dataset):

    def load_custom(self, dataset_dir, subset):
        """Load a subset of the bottle dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # Add classes. We have only one class to add.
        for i in range(1, len(class_names) + 1):
            self.add_class(category, i, class_names[i - 1] + 1)

        # Train or validation dataset?
        assert subset in ["train", "val"]
        dataset_dir = os.path.join(dataset_dir, subset)

        # Load annotations
        # VGG Image Annotator saves each image in the form:
        # { 'filename': '28503151_5b5b7ec140_b.jpg',
        #   'regions': {
        #       '0': {
        #           'region_attributes': {},
        #           'shape_attributes': {
        #               'all_points_x': [...],
        #               'all_points_y': [...],
        #               'name': 'polygon'}},
        #       ... more regions ...
        #   },
        #   'size': 100202
        # }
        # We mostly care about the x and y coordinates of each region

        coco = COCO(os.path.join(dataset_dir, 'annotations.json'))

        category_ids = coco.loadCats(coco.getCatIds())
        cat_ids = [obj['id'] for obj in category_ids]

        for catIndex in tqdm(cat_ids):
            image_ids = coco.getImgIds(catIds=catIndex)
            for i in range(len(image_ids)):
                polygons = []
                class_ids = []

                tmp = coco.loadImgs([image_ids[i]])
                w, h = tmp[0]['width'], tmp[0]['height']
                a_image_id = image_ids[i]
                img = coco.loadImgs(a_image_id)[0]  # here fetching it
                annotation_ids = coco.getAnnIds(imgIds=img['id'])
                annotations = coco.loadAnns(annotation_ids)
                image_path = os.path.join(dataset_dir, 'images/' + img['file_name'])

                # we are now inputting the polygons
                for j in range(len(annotations)):
                    all_points_x = []
                    all_points_y = []

                    for n in range(0, len(annotations[j]['segmentation'][0]), 2):
                        all_points_x.append(annotations[j]['segmentation'][0][n])
                        all_points_y.append(annotations[j]['segmentation'][0][n + 1])
                    polygons.append({'name': 'polygon', 'all_points_x': all_points_x, 'all_points_y': all_points_y})
                    idx = cat_ids.index(annotations[j]['category_id'])
                    class_ids.append(class_names.index(category_ids[idx]['name']) + 1)

                self.add_image(
                    category,  ## for a single class just add the name here
                    image_id=img['file_name'],  # use file name as a unique image id
                    path=image_path,
                    width=w, height=h,
                    polygons=polygons,
                    class_ids=class_ids)

    # TOMODIFY FROM HERE
    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        # If not a bottle dataset image, delegate to parent class.
        image_info = self.image_info[image_id]
        if image_info["source"] != category:
            return super(self.__class__, self).load_mask(image_id)

        class_ids = image_info['class_ids']
        # Convert polygons to a bitmap mask of shape
        # [height, width, instance_count]
        info = self.image_info[image_id]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            # rr, cc = skimage.draw.ellipse(p['cy'], p['cx'], p['ry'], p['rx'])
            mask[rr, cc, i] = 1

        # Return mask, and array of class IDs of each instance.
        class_ids = np.array(class_ids, dtype=np.int32)
        return mask.astype(np.bool), class_ids

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == category:
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)



#######################################################################################################################

def detect_and_color_splash(model, image=None):
    import cv2
    # Run model detection and generate the color splash effect
    #print("Running on {}".format(args.image))
    rgb_img = image.copy()

    # Detect objects
    r = model.detect([image], verbose=1)[0]


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

    filename = "crop_mask.jpg"
    cv2.imwrite(filename, image)

    return image, rgb_img



############################################################
#  Inference
############################################################
class InferenceConfig(CustomConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


def load_mrcnn_model():
    ### Define weights path
    # weights_path = './mask_rcnn/weights/mask_rcnn_head_final.h5'
    weights_path = os.path.join('./weights', "mask_rcnn_head_final.h5")
    print("Weights: ", weights_path)

    ### Define config
    config = InferenceConfig()
    #config.display()

    # Define Mask RCNN model
    model = modellib.MaskRCNN(mode="inference", config=config,
                                  model_dir='./logs')


    # Load weights
    print("Loading weights ", weights_path)
    model.load_weights(weights_path, by_name=True)


    return model

# global model
# model = load_mrcnn_model()
#
# detect_and_color_splash(model)


