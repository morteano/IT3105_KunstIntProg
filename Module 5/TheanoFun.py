from basics.mnist_basics import *

import numpy

helmerPath = "/Users/Butikk/.PyCharm40/AI 5/IT3105_KunstIntProg/Module 5/basics/"

case = load_cases("demo_prep", helmerPath, True)

images, labels = load_mnist("training", numpy.arange(10), helmerPath)

quicktest(1)