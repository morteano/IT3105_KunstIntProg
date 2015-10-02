import time
import heapq

colors = {0: "blue", 1: "red", 2: "green", 3: "yellow", 4: "purple", 5: "orange", 6: "pink", 7: "black", 8: "gray", 9: "lightGreen"}
# TODO: Fit in window. Maybe search through the file first!

from graphics import *
from Constraint import *
from copy import deepcopy

class Node:
    def __init__(self, nr, xPos, yPos):
        self.id = nr
        self.xPos = xPos
        self.yPos = yPos

        #textual representation of node, used for the general makefunc function
        self.text = 'n' + str(nr)

class HeapQueue: #Priority queue with heap as data structure
	def __init__(self):
		self.elements = []

	def empty(self):
		return len(self.elements) == 0

	def put(self, item, priority): #adds element to the heap
		heapq.heappush(self.elements, (priority, item))

	def get(self): #returns the element with lowest value and removes it from the heap
		return heapq.heappop(self.elements)[1]

class CSP:
    def __init__(self):
        # self.variables is a list of the variables in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.queue = []

        #keeps track of how many nodes that have only one value in their domain,
        #when this reaches the amount of nodes, the csp is solved
        self.progress = 0

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

        toBeDeleted = []

        func = self.makefunc(variableTexts, constraint.expression)

        if len(variablesInvolved) == 2:
            for j in self.domains[variablesInvolved[0]]:
                for k in self.domains[variablesInvolved[1]]:
                    if func(j, k):
                        break
                else:
                    toBeDeleted.append(j)
                    if len(self.domains[variable]) == 1:
                        self.progress += 1
                    modified = True
            for j in toBeDeleted:
                self.domains[variable].remove(j)
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

    def isSolved(self):
        if self.progress >= len(self.variables):
            return True
        return False




def create_csp(filename, numColors):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()

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
        for j in range(numColors):
            csp.domains[i].append(colors[j])
    return csp

# Find the extreme points in the graph
def extremePoint(csp):
    minX = csp.variables[0].xPos
    minY = csp.variables[0].yPos
    maxX = csp.variables[0].xPos
    maxY = csp.variables[0].yPos
    for var in csp.variables:
        if var.xPos < minX:
            minX = var.xPos
        elif var.xPos > maxX:
            maxX = var.xPos
        if var.yPos < minY:
            minY = var.yPos
        elif var.yPos > maxY:
            maxY = var.yPos
    return minX, maxX, minY, maxY


# Finds the smallest domain
def bestChoice(csp, numColors):
    domainSize = numColors + 1
    var = csp.variables[0]
    for i in csp.variables:
        if domainSize > len(csp.domains[i]) > 1:
            domainSize = len(csp.domains[i])
            var = i
    return var


def heuristic(csp):
    value = len(csp.variables)
    for i in csp.variables:
        if len(csp.domains[i]) == 1:
            value -= 1
        if len(csp.domains[i]) == 0:
            value += len(csp.variables)
    return value

def solveGraph(graph, numColors):
    startCsp = create_csp(graph, numColors)

    #is the solved csp
    resultCsp = startCsp

    numNodesInTree = 1

    numPoppedNodes = 0

    cameFrom = {}

    startCsp.initializeQueue()

    #priority queue containing csps
    openCsps = HeapQueue()

    openCsps.put(startCsp, heuristic(startCsp))

    #keeps track of graphical circles and what color they have
    graphicCircles = []

    minX, maxX, minY, maxY = extremePoint(startCsp)
    nodeDistance = 600/(maxX-minX)
    if minX < 0:
        shiftDistance = 20-minX*nodeDistance
    else:
        shiftDistance = 20

    win = GraphWin("CSP", 650, 650)
    for i in startCsp.variables:
        # Draw edges
        for neighbour in startCsp.constraints[i]:
            line = Line(Point(i.xPos * nodeDistance + shiftDistance, i.yPos * nodeDistance + shiftDistance), Point(neighbour.variables[1].xPos * nodeDistance + shiftDistance, neighbour.variables[1].yPos * nodeDistance + shiftDistance))
            line.draw(win)
        # Draw nodes
        circle = Circle(Point(i.xPos * nodeDistance + shiftDistance, i.yPos * nodeDistance + shiftDistance), 5)
        graphicCircles.append([circle, "white"])
        circle.draw(win)

    while True:
        currentCsp = openCsps.get()

        numPoppedNodes += 1

        #color vertices that only has one value in their domain
        for i in currentCsp.variables:
            if len(currentCsp.domains[i]) == 1:
                color = currentCsp.domains[i][0]
                if graphicCircles[i.id][1] != color:
                    graphicCircles[i.id][0].setFill(color)
                    graphicCircles[i.id][1] = color
        if currentCsp.isSolved():
            resultCsp = currentCsp
            break

        #add all neighbour csps to the priority queue
        #every neighbour to the current csp contains a different color of tempVar
        tempVar = bestChoice(currentCsp, numColors)
        for i in range(len(currentCsp.domains[tempVar])):
            nextCsp = deepcopy(currentCsp)

            nextVar = bestChoice(nextCsp, numColors)
            nextCsp.domains[nextVar] = [nextCsp.domains[nextVar][i]]
            nextCsp.progress += 1
            nextCsp.rerun(nextVar)
            nextCsp.domainFilter()

            numNodesInTree += 1

            cameFrom[nextCsp] = currentCsp
            openCsps.put(nextCsp, heuristic(nextCsp))


    #messy way of finding number of unsatisfied constraints. Should be 0
    numUnsatisfiedConstraints = 0
    for i in resultCsp.variables:
        for j in resultCsp.constraints[i]:

            variableTexts = []
            variablesInvolved = j.variables
            for k in variablesInvolved:
                variableTexts.append(k.text)

            func = resultCsp.makefunc(variableTexts, j.expression)

            if len(variablesInvolved) == 2:
                for l in resultCsp.domains[variablesInvolved[0]]:
                    for m in resultCsp.domains[variablesInvolved[1]]:
                        if not func(l, m):
                            numUnsatisfiedConstraints += 1

    #check how many uncolored vertices there are. Should be 0
    numUncoloredCircles = 0
    for i in resultCsp.variables:
        if graphicCircles[i.id][1] == "white":
            numUncoloredCircles += 1

    #find length of path from start to goal,
    #for some reason it always return numPoppedNodes - 1
    current = resultCsp
    pathLength = 0
    while current != startCsp:
        current = cameFrom[current]
        pathLength += 1

    print("Number of unsatisfied constraints: " + str(numUnsatisfiedConstraints))
    print("Number of uncolored vertices: " + str(numUncoloredCircles))
    print("Number of nodes in search tree: " + str(numNodesInTree))
    print("Number of nodes popped from agenda: " + str(numPoppedNodes))
    print("Length of path from root csp to solved csp: " + str(pathLength))

    win.getMouse()
    win.close()


def run():
    graph = raw_input("Graph name: ")
    numColors = raw_input("Number of colors: ")
#    nodeDistance = raw_input("Distance between nodes: ")
#    shiftDistance = raw_input("Distance to shift all nodes: ")

    solveGraph(graph, int(numColors))

run()