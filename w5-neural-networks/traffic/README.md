# Neural network that recognizes German traffic signs (CS50AI week 4 exercise)

## Background (copied from https://cs50.harvard.edu/ai/2020/projects/5/traffic/#background)

As research continues in the development of self-driving cars, one of the key challenges is computer vision, allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

In this project, you’ll use TensorFlow to build a neural network to classify road signs based on an image of those signs. To do so, you’ll need a labeled dataset: a collection of images that have already been categorized by the road sign represented in them.

Several such data sets exist, but for this project, we’ll use the [German Traffic Sign Recognition Benchmark (GTSRB)](http://benchmark.ini.rub.de/?section=gtsrb&subsection=news) dataset, which contains thousands of images of 43 different kinds of road signs.

### opencv-python

.. is also used (read more: https://www.geeksforgeeks.org/opencv-python-tutorial/)

## Data is not in the repository

It can be downloaded here: https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip

## How to run it

- `python traffic.py gtsrb`
- if you want to save the trained model: `python traffic.py gtsrb trained-model.h5`

## Experimentation process

- Since the nn expects images of the same size, they need to be resized. Therefore, I log the maximum dimensions of any file in the dataset (if the training variable is set to True), which should help me tweak the image dimensions (IMG_WIDTH and IMG_HEIGHT constants)
