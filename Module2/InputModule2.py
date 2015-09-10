
#TODO add more colors
K = 4
nodeDistance = .05
shiftDistance = 0
deadEnd = False

colors = {0: "blue", 1: "red", 2: "green", 3: "yellow", 4: "purple", 5: "orange"}

from graphics import *
from Constraint import *
from random import randint
from copy import deepcopy


class Node:
    def __init__(self, nr, xPos, yPos):
        self.id = nr
        self.xPos = xPos
        self.yPos = yPos

        #textual representation of node, used for the general makefunc function
        self.text = 'n' + str(nr)


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.queue = []

    def printConstraints(self, variable):
        for i in self.constraints[variable]:
            print(i.expression)


    # func = makefunc(['x', 'y', 'z'], 'x + y < 2*z')
    def makefunc(self, varNames, expression, envir=globals()):
        args = ""
        for n in varNames: args = args + "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")", envir)

    #not general yet, because it only works for constraints involving two variables,
    #need one extra for loop for each additional variable
    def revise(self, variable, constraint):
        modified = False

        variableTexts = []
        variablesInvolved = constraint.variables
        for j in variablesInvolved:
            variableTexts.append(j.text)

        func = self.makefunc(variableTexts, constraint.expression)

        if len(variablesInvolved) == 2:
            for j in self.domains[variablesInvolved[0]]:
                for k in self.domains[variablesInvolved[1]]:
                    if func(j, k):
                        break
                else:
                    self.domains[variable].remove(j)
                    if len(self.domains[variable]) == 0:
                        global deadEnd
                        deadEnd = True
                        break
                    modified = True
        return modified

    #initialize the queue containing variables and constraint pairs to filter variable domains
    def initializeQueue(self):
        for i in self.variables:
            for j in self.constraints[i]:
                self.queue.append((i, j))

    #filter the variable domains until no more deductions can be made
    def domainFilter(self):
        while self.queue:
            varConsTuple = self.queue.pop(0)
            currentVariable = varConsTuple[0]
            currentConstraint = varConsTuple[1]



            if self.revise(currentVariable, currentConstraint):
                for i in self.constraints[currentVariable]:
                    if i != currentConstraint:
                        self.queue.append((currentVariable, i))

    def rerun(self, variable):
        for i in self.constraints[variable]:
            for j in range(len(i.variables)):
                if i.variables[j] != variable:
                    for k in self.constraints[i.variables[j]]:
                        if k.contains(variable):
                            self.queue.append((i.variables[j], k))





def create_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    #board = map(lambda x: x.strip(" "), open(filename, 'r'))

    file = open(filename)
    firstLine = file.readline().split(" ")
    NV = int(firstLine[0])  # Number of vertices
    NE = int(firstLine[1])  # Number of edges

    # Add nodes to csp.variables
    for i in range(NV):
        line = file.readline().split(" ")
        node = Node(int(line[0]), float(line[1]), float(line[2]))
        csp.variables.append(node)
        # Insert lists to the constraints dictionary
        csp.constraints[node] = []

    # Add neighbours to csp.constraints
    for i in range(NE):
        line = file.readline().split(" ")

        #nodeNr0 is the node in variables with id = line[0], same with nodeNr1
        nodeNr0 = csp.variables[int(line[0])]
        nodeNr1 = csp.variables[int(line[1])]

        #add constraint instance for nodeNr0 where NodeNr0 and nodeNr1 are involved and the last argument is
        #the constraint expression between the variables
        csp.constraints[nodeNr0].append(Constraint([nodeNr0, nodeNr1], nodeNr0.text + ' != ' + nodeNr1.text))
        csp.constraints[nodeNr1].append(Constraint([nodeNr1, nodeNr0], nodeNr1.text + ' != ' + nodeNr0.text))

    # Add K elements as domain of the nodes
    for i in csp.variables:
        csp.domains[i] = []
        for j in range(K):
            csp.domains[i].append(colors[j])
    return csp


# Finds the smallest domain
def bestChoice(csp):
    domainSize = K + 1
    var = csp.variables[0]
    for i in csp.variables:
        if domainSize > len(csp.domains[i]) > 1:
            domainSize = len(csp.domains[i])
            var = i
    return var


# Choose a value for the best chose of variable
def chooseBestChoice(csp):
    oldCsp = deepcopy(csp)
    var = bestChoice(csp)

    #old variables in old csp which corresponds to new variable in new csp
    oldVar = oldCsp.variables[var.id]

    index = randint(0, len(csp.domains[var])-1)
    csp.domains[var] = [csp.domains[var][index]]
    return var, oldVar, oldCsp, index



def displayGraph(csp):
    win = GraphWin("CSP", 650, 600)

    for i in csp.variables:
        # Draw edges
        for neighbour in csp.constraints[i]:
            line = Line(Point(i.xPos * nodeDistance + shiftDistance, i.yPos * nodeDistance + shiftDistance), Point(neighbour.variables[1].xPos * nodeDistance + shiftDistance, neighbour.variables[1].yPos * nodeDistance + shiftDistance))
            line.draw(win)
        # Draw nodes
        circle = Circle(Point(i.xPos * nodeDistance + shiftDistance, i.yPos * nodeDistance + shiftDistance), 5)
        if len(csp.domains[i]) == 1:
            csp.domainFilter()
            circle.setFill(csp.domains[i][0])  # circle.setFill(colors[csp.domains[0]])
        circle.draw(win)

    win.getMouse()
    win.close()

csp = create_csp("graph6")

csp.initializeQueue()
csp.domainFilter()
"""
csp.domains[csp.variables[1]] = ["blue"]
csp.domains[csp.variables[2]] = ["red"]
csp.domains[csp.variables[5]] = ["green", "red"]
csp.domains[csp.variables[4]] = ["yellow"]
csp.domains[csp.variables[9]] = ["purple"]
csp.domains[csp.variables[7]] = ["green"]
csp.domains[csp.variables[8]] = ["blue", "purple"]"""


oldCsps = []
#IT WORKS!
#solving graph 6 takes about 30-40 seconds
for i in range(500):
    var, oldVar, oldCsp, index = chooseBestChoice(csp)

    #var and old var are different node instances since they represent the same node but in different csps,
    #thats why we got the KeyError since we tried to reference var in old csp with the same var in new csp

    #add old csp to previos csps list
    oldCsps.append(oldCsp)

    #reduce the same domain of the old csp as the domain to the variable we chose in new csp
    oldCsp.domains[oldVar].pop(index)
    csp.rerun(var)
    csp.domainFilter()
    if deadEnd == True:
        csp = oldCsps.pop()
        deadEnd = False

        csp.domainFilter()

displayGraph(csp)








