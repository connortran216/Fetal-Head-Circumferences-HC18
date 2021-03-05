# Fetal Head Circumferences using HC18 dataset

This is a demo API which helps detecting the fetal head (Using Mask-RCNN) and measure its size (Using pure OpenCV toolkit) base on the given data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites & Install

Firstly, Install requirements dependencies using requirements.txt

pip install -r requirements.txt

Remember, Mask-RCNN is the fork from https://github.com/matterport/Mask_RCNN which still using TF1 for training, but I still use TF2 for inferencing.

Secondly, Install docker and docker-compose for deployment

## Deployment in Docker

Run docker-compose file to build and start 5 containers

docker-compose up -f

## Testing the API

Simply run test_api.py to test.

Notice: The dataset is not included, you can download it from https://hc18.grand-challenge.org/


## Authors

Researcher - Developer: *Tran Tuan Canh* 
Instructor: *PhD. Le Minh Hung*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Basic Machine Learning, Deep Learning
* Basic Python on Image Processing, FastAPI, Tensorflow framework, 
* Basic Docker or others deployment formats
