import theano
import theano.tensor as T
import theano.tensor.nnet as Tann

import numpy as np

def genallbitcases(numbits):
    def bits(n):
        s = bin(n)[2:]
        return [int(b) for b in '0' *(numbits - len(s)) + s]
    return [ bits(i) for i in range(2**numbits)]

class autoencoder:
    def init(self, nb=3, nh=2, lr=.1):
        self.cases = genallbitcases(nb)
        self.lrate = lr
        self.buildann(nb, nh, lr)

    def buildann(self, nb, nh, lr):
        w1 = theano.shared(np.random.uniform(-.1, .1, size = (nb, nh)))
        w2 = theano.shared(np.random.uniform(-.1, .1, size = (nh, nb)))
        input = T.dvector ('input')
        b1 = theano.shared(np.random.uniform(-.1, .1, size = nh))
        b2 = theano.shared(np.random.uniform(-.1, .1, size = nb))
        x1 = Tann.sigmoid(T.dot(input, w1) + b1)
        x2 = Tann.sigmoid(T.dot(x1, w2) + b2)
        error = T.sum((input - x2)**2)
        params = [w1, b1, w2, b2]
        gradients = T.grad(error, params)
        backprop_acts = [(p, p - self.lrate * g) for p,g in zip(params, gradients)]
        self.predictor = theano.function([input], [x2, x1])
        self.trainer = theano.function([input], error, updates = backprop_acts)

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
