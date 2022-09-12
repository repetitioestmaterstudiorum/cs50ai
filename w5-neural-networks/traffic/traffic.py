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
    training = False # true while working on training the model
    image_limit = None # any natural number (0, 1, ...) or None

    cwd = os.getcwd()
    absolute_data_dir = os.path.join(cwd, data_dir)

    category_names = list() # returned as labels from this function
    images = []
    
    # capture largest dimensions in the data for parameter optimization
    max_width = 0
    max_height = 0

    # index for development purposes
    i = 0

    for category in os.scandir(absolute_data_dir):
        # exclude .DS_Store, etc.
        if not category.is_dir() or not category.name.isdigit():
            continue

        for file in os.scandir(category.path):
            # exclude .DS_Store, etc.
            if not file.name.endswith('.ppm'): 
                continue

            img = cv2.imread(file.path) # type: numpy.ndarray
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

            category_names.append(category.name)
            images.append(img)

            # in training, capture max width and height to adjust resize dimensions during training the model
            if training:
                if img.shape[1] > max_width:
                    max_width = img.shape[1] 
                if img.shape[0] > max_height:
                    max_height = img.shape[0]
            
            if image_limit:
                if i > image_limit:
                    break
                i += 1

    training and print(f">>>> max_width: {max_width}, max_height: {max_height}\n")

    hacking and print(f"category_names found: {len(category_names)}, {set(category_names)}")
    hacking and print(f"images found: {len(images)}")

    return (images, category_names)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([

        # change from RGB coefficients to 0-1 values
        tf.keras.layers.Rescaling(1.0 / 255), # this makes a huge difference!

        # convolutional layer: 32 filters using a 3x3 kernel
        tf.keras.layers.Conv2D(32, (4, 4), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # max-pooling layer with a 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(3, 3)),
        
        # flatten the units
        tf.keras.layers.Flatten(),

        # hidden layer and dropout to not overfit
        tf.keras.layers.Dense(200, activation="sigmoid"),
        tf.keras.layers.Dropout(0.5),

        # output layer with as many output layers as traffic sign categories
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # train the nn model
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
