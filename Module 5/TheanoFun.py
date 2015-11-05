from basics.mnist_basics import *
from LogisticRegression import *

import numpy
import theano
import theano.tensor as T

helmerPath = "/Users/Butikk/.PyCharm40/AI 5/IT3105_KunstIntProg/Module 5/basics/"

case = load_cases("demo_prep", helmerPath, True)

images, labels = load_mnist("training", numpy.arange(10), helmerPath)

print(images.dtype)

def filter(image):
    for j in image:
        for k in range(len(j)):
            j[k] /= 255.0
    return image

def filterAll(images):
    images = images.astype(float)
    for i in range(len(images)):
        images[i] = filter(images[i])
    return images

images = filterAll(images);
print(images.dtype)
print(images[0])


# generate symbolic variables for input (x and y represent a
# minibatch)
x = T.matrix('x')  # data, presented as rasterized images
y = T.ivector('y')  # labels, presented as 1D vector of [int] labels

# construct the logistic regression class
# Each MNIST image has size 28*28
classifier = LogisticRegression(images, n_in=28 * 28, n_out=10)

