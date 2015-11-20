from basics.mnist_basics import *

import numpy as np
import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import matplotlib.pyplot as plt

import time
import pickle

def createCompVector(label):
    vector = []
    for i in range(4):
        vector.append(0)
    vector[label] = 1
    return vector

def relu(x):
    return theano.tensor.switch(x<0, 0, x)

class ann:
    #initiate values, and start building the neural network.
    #since there can be several layers of hidden nodes, nh is an array with amount of nodes in the corresponding layer
    def __init__(self, images, labels, ni=17, nh=[10, 8], no=4, lr=.1):
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
        for i in range(len(nh)):
            if i == 0:
                x.append(Tann.hard_sigmoid(T.dot(input, self.w[i]) + self.b[i]))
            x.append(Tann.hard_sigmoid(T.dot(x[i], self.w[i + 1]) + self.b[i + 1]))

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
                for k in range(4):
                    if maxValue < xLast[k]:
                        maxValue = xLast[k]
                        maxIndex = k
                if maxIndex != labels[j]:
                    mistakes += 1
                totalError += error
                j += 1

            errors.append(totalError)
            print("Error", totalError)
            print("Amount of mistakes", mistakes, "/", len(self.cases))
            print("Percentage", 1-mistakes/len(self.cases))
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
            for k in range(4):
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
            for k in range(4):
                if maxValue < xLast[k]:
                    maxValue = xLast[k]
                    maxIndex = k
            finalResult.append(maxIndex)
        return finalResult

    def blind_test_restricted(self, feature_sets, dir):
        finalResult = []
        dirs = []
        for d in dir:
            print(d)
            if d == 'w':
                dirs.append(0)
            elif d == 'd':
                dirs.append(1)
            elif d == 's':
                dirs.append(2)
            elif d == 'a':
                dirs.append(3)
        for c in feature_sets:
            xLast = self.predictor(c)
            maxValue = -1
            maxIndex = -1
            for k in range(4):
                if maxValue < xLast[k] and k not in dirs:
                    maxValue = xLast[k]
                    maxIndex = k
            print("Something", maxIndex, dirs)
            finalResult.append(maxIndex)
        return finalResult


def runTraining(ni = 17, nh = [17, 17, 17, 17], no = 4, lr = .1):
    #load the training dataset
    file = open("ExtraInfoBadMoves", 'rb')
    data = pickle.load(file)
    file.close()
    boards = []
    moves = []
    i = 0
    for line in data:
        board = []
        for i in range(len(line[0])):
            board.append(line[0][i]/max(line[0]))
        boards.append(board)
        if line[1] == 'w':
            moves.append(0)
        elif line[1] == 'd':
            moves.append(1)
        elif line[1] == 's':
            moves.append(2)
        elif line[1] == 'a':
            moves.append(3)
        if i >= len(data)-100:
            break
        i += 1

    #create and train the neural network
    network = ann(boards, moves, ni, nh, no, lr)
    error = network.dotraining(moves, 100)

    #save the trained network
    file = open("trainedAnnBadmoves", 'wb')
    pickle.dump(network, file, protocol=pickle.HIGHEST_PROTOCOL)
    file.close()

    return error

def runTesting():
    #load the trained network
    file = open("trainedAnnBadmoves", 'rb')
    network = pickle.load(file)
    file.close()

    #load the testing dataset
    file = open("ExtraInfoBadMoves", 'rb')
    data = pickle.load(file)
    file.close()
    print(len(data))
    boards = []
    moves = []
    for i in range(len(data)-100, len(data)):
        line = data[i]
        board = []
        for i in range(len(line[0])):
            board.append(line[0][i]/max(line[0]))
        boards.append(board)
        if line[1] == 'w':
            moves.append(0)
        elif line[1] == 'd':
            moves.append(1)
        elif line[1] == 's':
            moves.append(2)
        elif line[1] == 'a':
            moves.append(3)

    #run the dataset through the trained neural network
    print(boards)
    result = network.blind_test(boards)

    #compare result with right answers and find the correctness percentage
    mistakes = 0
    for i in range(len(result)):
        if result[i] != moves[i]:
            mistakes += 1

    print("Test mistakes", mistakes)
    print("Percentage", 1 - (mistakes / len(result)))

def selectMove(board):
    # Get stored network
    file = open("trainedAnn", 'rb')
    network = pickle.load(file)
    file.close()

    # Filter
    networkBoard = [[]]
    for i in range(len(board[0])):
        networkBoard[0].append(board[0][i]/max(board[0]))

    # Make input ready for insertion
    if max(board[0]) == board[0][0]:
        element = 2048
    elif max(board[0]) == board[0][3]:
        element = 1536
    elif max(board[0]) == board[0][15]:
        element = 1024
    elif max(board[0]) == board[0][11]:
        element = 512
    else:
        element = 0.0
    networkBoard[0].append(element)

    # Get a move using the network
    moveNum = network.blind_test(networkBoard)
    print(moveNum)
    possibilities = ["w","d","s","a"]
    move = possibilities[moveNum[0]]
    return move

def selectOtherMove(board, dir, network):
    # Filter
    networkBoard = [[]]
    for i in range(len(board[0])):
        networkBoard[0].append(board[0][i]/max(board[0]))

    # Make input ready for insertion
    if max(board[0]) == board[0][0]:
        element = 2048
    elif max(board[0]) == board[0][3]:
        element = 1536
    elif max(board[0]) == board[0][15]:
        element = 1024
    elif max(board[0]) == board[0][11]:
        element = 512
    else:
        element = 0.0
    networkBoard[0].append(element)

    # Get a move using the network
    moveNum = network.blind_test_restricted(networkBoard, dir)
    print(moveNum)
    possibilities = ["w","d","s","a"]
    move = possibilities[moveNum[0]]
    print(move)
    return move

# error = runTraining(17, [15, 10], 4, .1)
# runTesting()
# selectMove([[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]])