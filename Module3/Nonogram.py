from graphics import *

from CSP import *
from Constraint import *
from copy import deepcopy

numberOfSegmentsInRows = 0

class Node:

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.filled = False

class Block:
    # Rows and columns
    def __init__(self, index, length, rowNumber):
        self.index = index
        self.rowNumber = rowNumber
        self.length = length
        self.text = 'b' + str(self.index)


def readCsp(textFile):
    csp = CSP()

    board = []

    file = open(textFile)

    firstLine = file.readline().split(" ")
    numberOfRows = int(firstLine[1])
    numberOfColumns = int(firstLine[0])
    domainX = range(numberOfRows)
    domainY = range(numberOfColumns)

    # Creates board
    for i in range(numberOfRows):
        board.append([])
        for j in range(numberOfColumns):
            board[i].append(Node(i, j))

    # Add start position for segments in rows
    counter = 0
    for i in range(numberOfRows):
        line = file.readline().split(" ")
        for j in line:
            block = Block(counter, int(j), i)
            counter += 1
            csp.variables.append(block)
            csp.constraints[block] = []
            csp.domains[block] = deepcopy(domainX)

    global numberOfSegmentsInRows
    numberOfSegmentsInRows = counter;

    # Add start position for segments in columns
    for i in range(numberOfColumns):
        line = file.readline().split(" ")
        for j in line:
            block = Block(counter, int(j), i)
            counter += 1
            csp.variables.append(block)
            csp.constraints[block] = []
            csp.domains[block] = deepcopy(domainY)

    # Add constraints to CSP
    for j in csp.variables:
        # Check if segment is the last
        if j.index == len(csp.variables) - 1:
            csp.constraints[j].append(Constraint([j], j.text + ' + ' + str(j.length) + ' <= ' + str(numberOfColumns)))
        # Segment is in a row
        elif j.index < numberOfSegmentsInRows:
            if j.rowNumber == csp.variables[j.index + 1].rowNumber:

                #j.text = 'b1'
                #str(j.length) = '2'
                #csp.variables[j.index + 1].text = 'b2'
                #'b1 + 2 < b2'
                csp.constraints[j].append(Constraint([j, csp.variables[j.index + 1]], j.text + ' + ' + str(j.length) + ' < ' + csp.variables[j.index + 1].text))
                csp.constraints[csp.variables[j.index + 1]].append(Constraint([csp.variables[j.index + 1], j], j.text + ' + ' + str(j.length) + ' < ' + csp.variables[j.index + 1].text))
            else:
                csp.constraints[j].append(Constraint([j], j.text + ' + ' + str(j.length) + ' <= ' + str(numberOfColumns)))
        # Segment is in a column
        else:
            if j.rowNumber == csp.variables[j.index + 1].rowNumber:
                csp.constraints[j].append(Constraint([j, csp.variables[j.index + 1]], j.text + ' + ' + str(j.length) + ' < ' + csp.variables[j.index + 1].text))
                csp.constraints[csp.variables[j.index + 1]].append(Constraint([csp.variables[j.index + 1], j], j.text + ' + ' + str(j.length) + ' < ' + csp.variables[j.index + 1].text))
            else:
                csp.constraints[j].append(Constraint([j], j.text + ' + ' + str(j.length) + ' <= ' + str(numberOfRows)))

    return csp



csp = readCsp("scenario0")



for i in csp.variables:
    for j in csp.constraints[i]:
        print(j.expression)

for i in csp.variables:
    print(csp.domains[i])
csp.initializeQueue()
csp.domainFilter()
print("\n")
for i in csp.variables:
    print(i.text, csp.domains[i])


