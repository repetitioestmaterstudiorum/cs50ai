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
- Same nn architecture (32 filter relu convolution, max-pooling with 2x2 pool size, flattening, 1 hidden layer with 128 relu nodes, dropout 50%, and a sigmoid activation output layer, compile with the adam optimizer and categorical_crossentropy loss function) as with the handwriting example performs pretty poorly: 0.0583 accuracy
- Training the nn on the GPU is slightly faster than on the CPU on an M1 processor
- Adding one hidden layers of 128 nodes: 0.0537 accuracy, CPU is not slightly faster to train
- Reverting to one hidden layer in total, but this time with 500 nodes: 0.0519 accuracy
- Since the accuracy does not seem to be influenced much by madding a hidden layer or increasing the amount of nodes, I decided to increase the epochs by an order of magnitude to 100: 0.0536 accuracy while testing. 0.0581 was achieved after 3 training epochs already and never increased
- Since the max image width and height of any image is 243 and 225, I increased the constants IMG_WIDTH and IMG_HEIGHT to 200 each, and returned to the initial settings otherwise: this increased the amount of data a lot. CPU & GPU still trained the model in more or less the same amount of time. Training accuracy seemed to get mostly stuck after 3 epochs again, at 0.0584.
  333/333 - 16s - loss: 3.5044 - accuracy: 0.0532 - 16s/epoch - 49ms/step
- A higher resolution does not seem to have a great effect. Reverting to 30 x 30. Also, since accuracy seems stable after just 3 epochs, reducing epochs to 5 for now. Next experiment: no pooling:
  333/333 - 1s - loss: 3.5081 - accuracy: 0.0526 - 650ms/epoch - 2ms/step
- 50 x 50 resolution, 2x2 kernel size convolution, no pooling:
  333/333 - 1s - loss: 3.5112 - accuracy: 0.0538 - 1s/epoch - 4ms/step
- Change the dropout to 20%:
  333/333 - 1s - loss: 3.5035 - accuracy: 0.0573 - 1s/epoch - 4ms/step
- Change the dropout back to 50%, increase the nodes to 500:
  333/333 - 8s - loss: 3.5116 - accuracy: 0.0535 - 8s/epoch - 24ms/step
- I noticed that I use a sigmoid activation function, but the goal is to get only one category to be true of false, so I switched to "softmax". Still width x height of 50, no pooling (optimization can happen last), and again with one hidden layer of 128 nodes, and 5 epochs:
  333/333 - 2s - loss: 3.5126 - accuracy: 0.0547 - 2s/epoch - 5ms/step
- Adding 3 layers of each 128 nodes:
  333/333 - 2s - loss: 3.5075 - accuracy: 0.0572 - 2s/epoch - 5ms/step
- Reverting to 1 hidden layer, switching to "tanh" activation:
  333/333 - 2s - loss: 3.5247 - accuracy: 0.0553 - 2s/epoch - 5ms/step
- Switching to a "sigmoid" activation function for the hidden layer:
  333/333 - 1s - loss: 3.5138 - accuracy: 0.0558 - 1s/epoch - 4ms/step
- Increase epochs to 10, since the last one was still better than the second last:
  333/333 - 1s - loss: 3.5060 - accuracy: 0.0530 - 1s/epoch - 4ms/step
- Increase epochs to 20 to make sure the model is stable
  333/333 - 1s - loss: 3.5156 - accuracy: 0.0512 - 1s/epoch - 4ms/step
  After epoch 6, a higher accuracy was already reached then after epoch 20.
- Reduce to 10 epochs, add 128 node layer and dropout after it, both sigmoid activations:
  333/333 - 2s - loss: 3.5063 - accuracy: 0.0539 - 2s/epoch - 5ms/step
- Adding another same layer and dropout:
  333/333 - 1s - loss: 3.5048 - accuracy: 0.0559 - 1s/epoch - 4ms/step
- Adding another same layer and dropout, now 4 in total:
  333/333 - 1s - loss: 3.5036 - accuracy: 0.0521 - 1s/epoch - 4ms/step
- Increase the epochs to 500 just to see what happens (and because it's lunch time so I won't have to wait on it):
  333/333 - 1s - loss: 3.5011 - accuracy: 0.0549 - 1s/epoch - 4ms/step
  The accuracy appears to be about the same in each experiment I conducted after 2 or 3 epochs. I think that something fundamental must be wrong (with my code) if I can't reach an accuracy of at least 80%
- I tested with a lower amount of data by reading only for example 1000 or 3000 images and their labels into the. I instantly reached an accuracy of 0.77 (with 1000 images) and 0.25 with 3000 images. This could be explained with a lower lable variance of the partial dataset, but not sure to what degree. I found a rookie mistake in my code: I used a set instead of a list to store the file paths. Since sets don't guarantee the order of the items, this could be the problem. Experiment with a list to store paths in the load_data function, and with almost base settings: 50x50 dimensions, 10 epochs, 1 hidden layer with sigmoid activation and 50% dropout, no pooling, output layer with softmax:
  333/333 - 1s - loss: 3.5070 - accuracy: 0.0546 - 1s/epoch - 4ms/step
  Unfortunately, the accuracy isn't higher when using all data.
- Reset default settings for image dimensions (30x30), add two more convolutional layers:
  333/333 - 2s - loss: 3.5142 - accuracy: 0.0547 - 2s/epoch - 5ms/step
- Running the same with 50 epochs:
  333/333 - 2s - loss: 3.5064 - accuracy: 0.0568 - 2s/epoch - 7ms/step
- Change code again to directly add a numpy ndarray image when adding a label to simplify the code and ensure the labels fit the images. Reset to 10 epochs:
  333/333 - 2s - loss: 3.5031 - accuracy: 0.0497 - 2s/epoch - 7ms/step
- Rerun it with 50 epochs because the earlier run with 50 epochs was better:
  333/333 - 2s - loss: 3.4992 - accuracy: 0.0586 - 2s/epoch - 7ms/step
  It seems that a slightly better result can be achieved with training 5 times longer, however, it's still a very poor result, so I'll revert to 5 epochs to see the difference with 10 epochs with this nn configuration:
  333/333 - 2s - loss: 3.5124 - accuracy: 0.0534 - 2s/epoch - 6ms/step
  It's even better than with 10 epochs. It seems like the number of epochs above 5 doesn't change much with this configuration. Other things must be improved. Reducing to 2 convolutional layers:
  333/333 - 1s - loss: 3.4983 - accuracy: 0.0576 - 1s/epoch - 4ms/step
- Reducing to 1 conv. layer:
  333/333 - 1s - loss: 3.5191 - accuracy: 0.0566 - 645ms/epoch - 2ms/step
- After researching online and reading differnt how-tos on image classification, I found my **silver bullet**: rescaling the images from 0-255 to 0-1. An explanation for this I found here: https://github.com/Arsey/keras-transfer-learning-for-oxford102/issues/1. The result after the adaptation:
  333/333 - 1s - loss: 0.0820 - accuracy: 0.9825 - 595ms/epoch - 2ms/step
  If I understand this correctly, each value of each numpy.ndarray will be multiplied by 1/255 to get a value between 0 and 1. This ensures that with a "typical learning rate", the model can learn properly. Open question: where is this learning rate defined and should I assume values should always be between 0 and 1 for nn models?
- Running the same with 5 epochs:
  333/333 - 1s - loss: 0.1776 - accuracy: 0.9675 - 555ms/epoch - 2ms/step
- Getting back to the initial tweaking. Increasing to 320 filters for the convolutional layer:
  333/333 - 2s - loss: 0.1236 - accuracy: 0.9762 - 2s/epoch - 7ms/step
- Reverting to 32 filters, but using a 2x2 kernel
  333/333 - 1s - loss: 0.2907 - accuracy: 0.9411 - 517ms/epoch - 2ms/step
- Trying a 4x4 kernel:
  333/333 - 1s - loss: 0.1596 - accuracy: 0.9660 - 564ms/epoch - 2ms/step
- And a 5x5 kernel:
  333/333 - 1s - loss: 0.1589 - accuracy: 0.9719 - 628ms/epoch - 2ms/step
- 6x6:
  333/333 - 1s - loss: 0.1701 - accuracy: 0.9714 - 557ms/epoch - 2ms/step
- Going back to 5x5, but 8 epochs:
  333/333 - 1s - loss: 0.0971 - accuracy: 0.9796 - 701ms/epoch - 2ms/step
- Back to 4x4:
  333/333 - 1s - loss: 0.0977 - accuracy: 0.9787 - 589ms/epoch - 2ms/step
- Back to 5x5, but now with a max-pooling pool size of 3x3 instead of 2x2:
  333/333 - 1s - loss: 0.1133 - accuracy: 0.9792 - 515ms/epoch - 2ms/step
- 5x5 pool:
  333/333 - 0s - loss: 0.2706 - accuracy: 0.9401 - 465ms/epoch - 1ms/step
- Traning seems to run faster but learn slower now. Increasing to 14 epochs:
  333/333 - 1s - loss: 0.1674 - accuracy: 0.9596 - 501ms/epoch - 2ms/step
- Returning to 3x3 pool (still with 32 4x4 filters), 14 epochs:
  333/333 - 0s - loss: 0.0672 - accuracy: 0.9838 - 492ms/epoch - 1ms/step
- Chaning the hidden sigmoid layer to 1000 nodes (from 128):
  333/333 - 1s - loss: 0.0592 - accuracy: 0.9868 - 1s/epoch - 3ms/step
- Barely any improvement but much more computation. Going back to 200:
  333/333 - 1s - loss: 0.0515 - accuracy: 0.9871 - 536ms/epoch - 2ms/step
- Adding another hidden layer with 200 nodes:
  333/333 - 1s - loss: 0.0909 - accuracy: 0.9777 - 564ms/epoch - 2ms/step
  The CPU is about twice as fast at processing this data now compared to the GPU.
- No improvement: back to 1 hidden layer. Dropout of 0.3 instead of 0.5:
  333/333 - 1s - loss: 0.0593 - accuracy: 0.9850 - 528ms/epoch - 2ms/step
- Dropout to 0.7:
  333/333 - 1s - loss: 0.0830 - accuracy: 0.9838 - 534ms/epoch - 2ms/step
- Worse. Back to 0.5, but add a dropout of 0.01 to the conv. layer:
  333/333 - 1s - loss: 0.0629 - accuracy: 0.9845 - 526ms/epoch - 2ms/step
  No improvement.
- relu instead of sigmoid for the hidden layer:
  333/333 - 1s - loss: 0.0681 - accuracy: 0.9854 - 533ms/epoch - 2ms/step
  More or less the same.
- Sigmoid for the conv. layer (and sigmoid again for the hidden layer):
  333/333 - 1s - loss: 0.1929 - accuracy: 0.9528 - 561ms/epoch - 2ms/step
- Worse, reverting to relu for the conv. layer:
  333/333 - 1s - loss: 0.0706 - accuracy: 0.9817 - 798ms/epoch - 2ms/step

The network is relatively simple, is trained quite fast, and classifies with ~98% accuracy.
