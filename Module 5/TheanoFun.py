from basics.mnist_basics import *
from LogisticRegression import *

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

class autoencoder:
    def __init__(self, images, labels, nb=10, nh=100, nob=10, lr=.1):
        self.cases = genallbitcases(nb)
        self.labels = labels
        self.lrate = lr
        self.buildann(nb, nh, nob, lr)

    def buildann(self, nb , nh, nob, lr):
        w1 = theano.shared(np.random.uniform(-.1, .1, size = (nb, nh)))
        w2 = theano.shared(np.random.uniform(-.1, .1, size = (nh, nob)))
        input = T.dvector ('input')
        label  = T.ivector ('label')
        b1 = theano.shared(np.random.uniform(-.1, .1, size = nh))
        b2 = theano.shared(np.random.uniform(-.1, .1, size = nob))
        x1 = Tann.sigmoid(T.dot(input, w1) + b1)
        x2 = Tann.sigmoid(T.dot(x1, w2) + b2)
        error = 0 if maxIndex(x2) == label else 1
        params = [w1, b1, w2, b2]
        gradients = T.grad(error, params)
        backprop_acts = [(p, p - self.lrate * g) for p,g in zip(params, gradients)]
        self.predictor = theano.function([input], [x2, x1])
        self.trainer = theano.function([label], error, updates = backprop_acts)

    def dotraining(self, epochs = 100):
        errors = []
        for i in range(epochs):
            error = 0
            for c in self.cases:
                error += self.trainer(c)
            errors.append(error)
        return errors

    def dotesting(self):
        hidden_activations = []
        for c in self.cases:
            hact = self.predictor(c)
            hidden_activations.append(hact)
        return hidden_activations

helmerPath = "/Users/Butikk/.PyCharm40/AI 5/IT3105_KunstIntProg/Module 5/basics/"
normannPath = "/Users/MortenAlver/PycharmProjects/IT3105_KunstIntProg/Module 5/basics/"

case = load_cases("demo_prep", normannPath, True)

images, labels = load_mnist("training", np.arange(10), normannPath)

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


flatImages = getFlatInput(images)
print("1")
auto = autoencoder(flatImages, labels)
error = auto.dotraining(100)
epochs = []
for i in range(len(error)):
    epochs.append(i)
hidden = auto.dotesting()

plt.plot(epochs, error)
plt.xlabel('epochs')
plt.ylabel('error')
plt.title('Result')
plt.show()

print(hidden)
plt.plot(*zip(*hidden), marker='o', color='r', ls='')
plt.show()