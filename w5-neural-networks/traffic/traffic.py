import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    hacking = False # true while developing
    training = True # true while working on training the model

    cwd = os.getcwd()
    absolute_data_dir = os.path.join(cwd, data_dir)

    category_names = list() # returned as labels from this function
    file_paths = set()

    for category in os.scandir(absolute_data_dir):
        if category.is_dir() and category.name.isdigit(): # ensure entry is a directory and its name a number (not .DS_Store, etc.)
            for file in os.scandir(category.path):
                if file.name.endswith('.ppm'): # ensure file ends with .ppm (not .DS_Store, etc.)
                    category_names.append(category.name)
                    file_paths.add(file.path)

    hacking and print(f"category_names found: {len(category_names)}, {category_names}")
    hacking and print(f"file_paths found: {len(file_paths)}")

    max_width = 0
    max_height = 0

    images = []

    for path in list(file_paths)[:10] if hacking else file_paths:
        img = cv2.imread(path) # type: numpy.ndarray
        hacking and print('original dimensions : ', img.shape)

        # capture max width and height to adjust resize dimensions during training the model
        if img.shape[1] > max_width:
            max_width = img.shape[1] 
        if img.shape[0] > max_height:
            max_height = img.shape[0]
        
        img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
        hacking and print('new dimensions : ', img.shape)

        images.append(img)
        
    training and print(f">>>> max_width: {max_width}, max_height: {max_height}\n")

    return (images, category_names)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
