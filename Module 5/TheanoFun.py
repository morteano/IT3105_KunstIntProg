from basics.mnist_basics import *
from LogisticRegression import *

import numpy as np
import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import matplotlib.pyplot as plt

import time

helmerPath = "/Users/Butikk/.PyCharm40/AI 5/IT3105_KunstIntProg/Module 5/basics/"
normannPath = "/Users/MortenAlver/PycharmProjects/IT3105_KunstIntProg/Module 5/basics/"

def genallbitcases(numbits):
    def bits(n):
        s = bin(n)[2:]
        return [int(b) for b in '0' *(numbits - len(s)) + s]
    return [ bits(i) for i in range(2**numbits)]

def createCompVector(label):
    vector = []
    for i in range(10):
        vector.append(0)
    vector[label] = 1
    return vector

class ann:
    def __init__(self, images, labels, ni=28**2, nh=100, no=10, lr=.1):
        self.cases = images
        self.labels = labels
        self.numInputNodes = ni
        self.numHiddenNodes = nh
        self.numOutputNodes = no
        self.lrate = lr
        self.buildann(ni, nh, no, lr)

    def buildann(self, nb , nh, nob, lr):
        w = []
        b = []
        x = []
        for i in range(len(nh)):
            if i == 0:
                w.append(theano.shared(np.random.uniform(-.1, .1, size = (nb, nh[i]))))
            if i != 0:
                w.append(theano.shared(np.random.uniform(-.1, .1, size = (nh[i - 1], nh[i]))))
            if i == len(nh) - 1:
                w.append(theano.shared(np.random.uniform(-.1, .1, size = (nh[i], nob))))
        input = T.dvector ('input')
        label = T.dvector ('label')
        for i in range(len(nh)):
            b.append(theano.shared(np.random.uniform(-.1, .1, size = nh[i])))
            if i == len(nh) - 1:
                b.append(theano.shared(np.random.uniform(-.1, .1, size = nob)))
        for i in range(len(nh)):
            if i == 0:
                x.append(Tann.sigmoid(T.dot(input, w[i]) + b[i]))
            x.append(Tann.sigmoid(T.dot(x[i], w[i + 1]) + b[i + 1]))
        error = T.sum((x[len(nh)] - label)**2)
        params = []
        for i in range(len(w)):
            params.append(w[i])
            params.append(b[i])
        #params = [w[0], b[0], w[1], b[1]]
        gradients = T.grad(error, params)
        backprop_acts = [(p, p - self.lrate * g) for p,g in zip(params, gradients)]
        self.predictor = theano.function([input], x[len(nh)])
        self.trainer = theano.function([input, label], [x[len(nh)], error], updates = backprop_acts)

    def dotraining(self, epochs = 100):
        errors = []
        start = time.time()
        for i in range(epochs):
            mistakes = 0
            totalError = 0
            j = 0
            for c in self.cases:
                xLast, error = self.trainer(c, createCompVector(labels[j]))
                maxValue = xLast[0]
                maxIndex = 0
                for k in range(10):
                    if maxValue < xLast[k]:
                        maxValue = xLast[k]
                        maxIndex = k
                if maxIndex != labels[j][0]:
                    mistakes += 1
                totalError += error
                j += 1
            errors.append(totalError)
            print("Error", totalError)
            print("Amount of mistakes", mistakes)
            print("Epoch", i)
        end = time.time()
        print("Total training time", end - start)
        return errors

    def dotesting(self):
        mistakeList = []
        for c in self.cases:
            mistakes = 0
            j = 0
            xLast = self.predictor(c)
            maxValue = xLast[0]
            maxIndex = 0
            for k in range(10):
                if maxValue < xLast[k]:
                    maxValue = xLast[k]
                    maxIndex = k
            if maxIndex != labels[j][0]:
                mistakes += 1
            j += 1
            mistakeList.append(mistakes)
        return mistakeList

    def blind_test(self, feature_sets):
        finalResult = []
        for c in feature_sets:
            xLast = self.predictor(c)
            maxValue = xLast[0]
            maxIndex = 0
            for k in range(10):
                if maxValue < xLast[k]:
                    maxValue = xLast[k]
                    maxIndex = k
            finalResult.append(maxIndex)
        return finalResult


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

case = load_cases("demo_prep", helmerPath, True)

images, labels = load_mnist("training", np.arange(10), helmerPath)

testImages, testLabels = load_mnist("testing", np.arange(10), helmerPath)

flatTestImages = getFlatInput(testImages)

flatImages = getFlatInput(images)
network = ann(flatImages, labels, 28**2, [50, 30], 10, .1)
error = network.dotraining(100)
"""epochs = []
for i in range(len(error)):
    epochs.append(i)"""
result = network.blind_test(flatTestImages)

mistakes = 0
for i in range(len(result)):

    if result[i] != testLabels[i]:
        mistakes += 1

print("Test mistakes", mistakes)
print("Percentage", 1 - (mistakes / len(result)))



"""plt.plot(epochs, error)
plt.xlabel('epochs')
plt.ylabel('error')
plt.title('Result')
plt.show()

plt.plot(*zip(*hidden), marker='o', color='r', ls='')
plt.show()"""