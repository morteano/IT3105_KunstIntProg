from basics.mnist_basics import *
from LogisticRegression import *

import numpy as np
import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import matplotlib.pyplot as plt

import time
import pickle

def createCompVector(label):
    vector = []
    for i in range(10):
        vector.append(0)
    vector[label] = 1
    return vector

def relu(x):
    return theano.tensor.switch(x<0, 0, x)

def softmax(X):
    e_x = T.exp(X - X.max(axis=1).dimshuffle(0, 'x'))
    return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')

class ann:
    #initiate values, and start building the neural network.
    #since there can be several layers of hidden nodes, nh is an array with amount of nodes in the corresponding layer
    def __init__(self, images, labels, ni=28**2, nh=[100], no=10, lr=.1):
        self.cases = images
        self.labels = labels
        self.numInputNodes = ni
        self.numHiddenNodes = nh
        self.numOutputNodes = no
        self.lrate = lr
        self.w = []
        self.b = []
        self.buildann(ni, nh, no, lr)

    #build the neural network
    def buildann(self, nb , nh, nob, lr):
        x = []

        #weights with initial random values between -0.1 and 0.1
        for i in range(len(nh)):
            if i == 0:
                self.w.append(theano.shared(np.random.uniform(-.1, .1, size = (nb, nh[i]))))
            if i != 0:
                self.w.append(theano.shared(np.random.uniform(-.1, .1, size = (nh[i - 1], nh[i]))))
            if i == len(nh) - 1:
                self.w.append(theano.shared(np.random.uniform(-.1, .1, size = (nh[i], nob))))

        #input is the image, label is the possible answers(0 to 9)
        input = T.dvector ('input')
        label = T.dvector ('label')

        #node values with initial random values between -0.1 and 0.1
        for i in range(len(nh)):
            self.b.append(theano.shared(np.random.uniform(-.1, .1, size = nh[i])))
            if i == len(nh) - 1:
                self.b.append(theano.shared(np.random.uniform(-.1, .1, size = nob)))

        #activation functions
        for i in range(len(nh)-1):
            if i == 0:
                x.append(relu(T.dot(input, self.w[i]) + self.b[i]))
            x.append(relu(T.dot(x[i], self.w[i + 1]) + self.b[i + 1]))
            print("inside",i)
        i = len(nh)-1
        print("outside", i)
        x.append(Tann.sigmoid(T.dot(x[i], self.w[i + 1]) + self.b[i + 1]))

        #error calculation, which gives least error for right guesses
        error = T.sum((x[len(nh)] - label)**2)

        #parameters needed for the gradient search
        params = []
        for i in range(len(self.w)):
            params.append(self.w[i])
            params.append(self.b[i])

        #gradient search
        gradients = T.grad(error, params)

        #backpropagation for updating weigths and node values
        backprop_acts = [(p, p - self.lrate * g) for p,g in zip(params, gradients)]

        #testing function
        self.predictor = theano.function([input], x[len(nh)])

        #training function
        self.trainer = theano.function([input, label], [x[len(nh)], error], updates = backprop_acts)

    #train the neural network. epochs is amount of iterations of training
    def dotraining(self, labels, epochs = 100):
        errors = []
        start = time.time()

        #backpropagates for every epoch, to train the neural network on the current dataset
        for i in range(epochs):
            mistakes = 0
            totalError = 0
            j = 0

            #checks if the guess for every case is right or wrong, and sums up the total amount of mistakes
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

    def dotesting(self, labels):
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

    #test the neural network on a testing dataset and return a list of all guesses
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

def runTraining(ni = 28**2, nh = [100], no = 10, lr = .1):
    #load the training dataset
    images, labels = load_mnist("training", np.arange(10))
    flatImages = getFlatInput(images)

    #create and train the neural network
    network = ann(flatImages, labels, ni, nh, no, lr)
    error = network.dotraining(labels, 100)

    #save the trained network
    file = open("trainedAnn", 'wb')
    pickle.dump(network, file, protocol=pickle.HIGHEST_PROTOCOL)
    file.close()

    return error

def runTesting(dataset):
    #load the trained network
    file = open("trainedAnn", 'rb')
    network = pickle.load(file)
    file.close()

    #load the testing dataset
    testImages, testLabels = load_mnist(dataset, np.arange(10))

    flatTestImages = getFlatInput(testImages)

    #run the dataset through the trained neural network
    result = network.blind_test(flatTestImages)

    #compare result with right answers and find the correctness percentage
    mistakes = 0
    for i in range(len(result)):

        if result[i] != testLabels[i]:
            mistakes += 1

    print("Test mistakes", mistakes, "/", len(result))
    print("Percentage", 1 - (mistakes / len(result)))

error = runTraining(28**2, [50, 30], 10, .1)
runTesting("training")
runTesting("testing")
#case = load_cases("demo_prep", helmerPath, True)

"""epochs = []
for i in range(len(error)):
    epochs.append(i)"""



"""plt.plot(epochs, error)
plt.xlabel('epochs')
plt.ylabel('error')
plt.title('Result')
plt.show()

plt.plot(*zip(*hidden), marker='o', color='r', ls='')
plt.show()"""