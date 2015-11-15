from basics.mnist_basics import *
from LogisticRegression import *
import time

import numpy as np
import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import matplotlib.pyplot as plt

def genallbitcases(numbits):
    def bits(n):
        s = bin(n)[2:]
        return [int(b) for b in '0' *(numbits - len(s)) + s]
    return [ bits(i) for i in range(2**numbits)]

def rectify(X):
    return T.maximum(X, 0.)

class autoencoder:
    def __init__(self, images, labels, testImages, testLabels, nb=28**2, nh=625, nob=10, lr=.01):
        self.cases = images
        self.labels = labels
        self.testCases = testImages
        self.testLabels = testLabels
        self.lrate = lr
        self.buildann(nb, nh, nob, lr)

    def buildann(self, nb , nh, nob, lr):
        w1 = theano.shared(np.random.uniform(-.1, .1, size = (nb, nh)))
        w2 = theano.shared(np.random.uniform(-.1, .1, size = (nh, nob)))
        input = T.dvector ('input')
        label  = T.dvector ('label')
        b1 = theano.shared(np.random.uniform(-.1, .1, size = nh))
        b2 = theano.shared(np.random.uniform(-.1, .1, size = nob))
        x1 = Tann.sigmoid(T.dot(input, w1) + b1)
        x2 = Tann.sigmoid(T.dot(x1, w2) + b2)
        error = T.sum((label-x2)**2)
        params = [w1, b1, w2, b2]
        gradients = T.grad(error, params)
        backprop_acts = [(p, p - self.lrate * g) for p,g in zip(params, gradients)]
        self.predictor = theano.function([input], x2)
        self.trainer = theano.function([input, label], x2, updates = backprop_acts)

    def dotraining(self, epochs = 100):
        errors = []
        for i in range(epochs):
            j = 0
            error = 0
            for c in self.cases:
                x2 = self.trainer(c, self.labels[j])
                # error += T.sum((labels[j]-x2)**2)
                maxVal = 0.0
                maxInt = 0
                for k in range(10):
                    if x2[k]>maxVal:
                        maxVal = x2[k]
                        maxInt = k
                    if labels[j][k] == 1:
                        labelInt = k
                if (labelInt != maxInt):
                    error += 1
                j += 1
            errors.append(error)
            print(i, error)

        return errors

    def dotesting(self):
        nrTests = 0
        error = 0
        for c in self.testCases:
            x2 = self.predictor(c)
            maxVal = 0.0
            maxInt = 0
            for k in range(10):
                if x2[k]>maxVal:
                    maxVal = x2[k]
                    maxInt = k
                if self.testLabels[nrTests][k] == 1:
                    labelInt = k
            if (labelInt != maxInt):
                error += 1
            nrTests += 1
        return error, nrTests


def maxIndex(x2):
    return 2


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

def getFlatInput(images):
    images = filterAll(images)
    flatImages = []
    for image in images:
        flatImages.append(flatten_image(image))
    return flatImages

def getLabelVectors(labels):
    labelVectors = []
    for label in labels:
        labelVector = [0]*10
        labelVector[label[0]] = 1
        labelVectors.append(labelVector)
    return labelVectors

helmerPath = "/Users/Butikk/.PyCharm40/AI 5/IT3105_KunstIntProg/Module 5/basics/"
normannPath = "/Users/MortenAlver/PycharmProjects/IT3105_KunstIntProg/Module 5/basics/"

case = load_cases("demo_prep", normannPath, True)

images, labels = load_mnist("training", np.arange(10), normannPath)
testImages, testlabels = load_mnist("testing", np.arange(10), normannPath)
startTime = time.time()
flatImages = getFlatInput(images)
flatTestImages = getFlatInput(testImages)

labels = getLabelVectors(labels)
testlabels = getLabelVectors(testlabels)
auto = autoencoder(flatImages, labels, flatTestImages, testlabels)
error = auto.dotraining(100)
epochs = []
for i in range(len(error)):
    epochs.append(i)
nrErrors, nrTests = auto.dotesting()
print(nrTests, nrErrors)
print((nrTests-nrErrors)/nrTests)
endTime = time.time()-startTime
print(endTime/60)
print("nh=625 lr=0.01")
plt.plot(epochs, error)
plt.xlabel('epochs')
plt.ylabel('error')
plt.title('Result')
plt.show()
