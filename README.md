# Fetal Head Circumferences using HC18 dataset

This is a demo API which helps detecting the fetal head (using Mask-RCNN) and measure its size (using Ramanujan’s formula) base on the given data.

## Getting Started

These instructions will get you a copy of the project and run it on your local machine for development and testing purposes. See deployment part to deploy the project on a live system.

### Prerequisites & Installation

Firstly, Install requirements dependencies using requirements.txt

*pip install -r requirements.txt*

Remember, Mask-RCNN is the fork from https://github.com/matterport/Mask_RCNN which still using TF1 for training, but I still use TF2 for inferencing.

Secondly, Install docker and docker-compose for deployment

## Deployment in Docker

Run docker-compose file to build and start 5 containers

*docker-compose up -d*

## Testing the API

Simply run test_api.py to test.

Notice: The testing dataset is not included, you can download it from https://hc18.grand-challenge.org/

## Mask Results

<img src="../master/Images/crop_mask.jpg" alt="Crop Mask" title="Crop Mask" width="250">  <img src="../master/Images/ellipse_on_crop_mask.jpg" alt="Ellipse on Crop Mask" title="Ellipse on Crop Mask" width="250">

For now, you can only check Head Circumference by looking for the logs inside Service Gateway container.

I'm still working on the Interface.

Use *docker logs container-name* to get the Result.

## HC18 Grand Challenge Results

To evaluation the whole system, we tested it with 335 ultrasound images, and then we
submitted the result to HC18 Grand Challenge.

As the result, we were ranked at 1077 position with several metrics as follow:

DICE:
* ”max”: 27.589732124216823
* ”min”: 76.75946495249799
* ”std”: 3.7815463871178943
* ”25pc”: 83.50825381011883
* ”50pc”: 85.81469956490609
* ”75pc”: 88.01129094018415
* ”mean”: 86.09170119968213
* ”count”: 335.0

Absolute difference:
* ”max”: 27.589732124216823
* ”min”: 0.6480596018764686
* ”std”: 4.3289838125839815
* ”25pc”: 4.394918205609386
* ”50pc”: 6.114941307429092
* ”75pc”: 8.74297314561646
* ”mean”: 7.151370067720037
* ”count”: 335.0

## Drawbacks and TO-DO

The whole system is running on CPU only so that the processing speed is limited. 

Therefore, in the future, the release version using GPU will improve the system performance.

Instead of using API design, we will employ message broker (or message brokerless) to deliver data among the cores.

As a result, not only it will speed up the process, but it is also available for scalability.

## Authors

Researcher - Developer: *Tran Tuan Canh* 

Instructor: *PhD. Le Minh Hung*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Basic Machine Learning, Deep Learning
* Basic Python on Image Processing, FastAPI, Tensorflow framework, 
* Basic Docker or others deployment formats
