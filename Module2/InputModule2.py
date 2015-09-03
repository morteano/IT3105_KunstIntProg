from Queue import Queue

K = 4
colors = {0: "blue", 1: "red", 2: "green", 3: "yellow", 4: "purple", 5: "orange"}

from graphics import *


class Node:
    def __init__(self, nr, xPos, yPos):
        self.id = nr
        self.xPos = xPos
        self.yPos = yPos


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = []

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

    def revise(self):
        magic = True

    def bestChoice(self):
        return max(self.heuristic())

    def heuristic(self):
        h = 0
        return h




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
        csp.constraints[i] = []

    # Add neighbours to csp.constraints
    for i in range(NE):
        line = file.readline().split(" ")
        nodeNr0 = int(line[0])
        nodeNr1 = int(line[1])
        csp.constraints[nodeNr0].append(csp.variables[nodeNr1])
        csp.constraints[nodeNr1].append(csp.variables[nodeNr0])

    # Add K elements as domain of the nodes
    for i in range(NV):
        csp.domains.append(range(K))

    return csp


def displayGraph(csp):
    win = GraphWin("CSP", 500, 500)
    for i in csp.variables:
        # Draw edges
        for neighbour in csp.constraints[i.id]:
            line = Line(Point(i.xPos * 20, i.yPos * 20), Point(neighbour.xPos * 20, neighbour.yPos * 20))
            line.draw(win)
        # Draw nodes
        circle = Circle(Point(i.xPos * 20, i.yPos * 20), 5)
        circle.setFill(colors[i.id % K])  # circle.setFill(colors[csp.domains[0]])
        circle.draw(win)

    win.getMouse()
    win.close()


# func = makefunc(['x', 'y', 'z'], 'x + y < 2*z')
def makefunc(var_names, expression, envir=globals()):
    args = ""
    for n in var_names: args = args + "," + n
    return eval("(lambda " + args[1:] + ": " + expression + ")", envir)



func = makefunc(['x', 'y'], 'x + y < 2*z')
displayGraph(create_csp("graph1"))