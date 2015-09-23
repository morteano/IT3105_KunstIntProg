from graphics import *

from CSP import *
from Constraint import *

class Node:

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.filled = False

class Block:

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

    counter = 0
    for i in range(int(firstLine[1])):
        board.append([])
        for j in range(int(firstLine[0])):
            board[i].append(Node(i, j))

    for i in range(int(firstLine[1])):
        line = file.readline().split(" ")
        for j in line:
            block = Block(counter, int(j), i)
            counter += 1
            csp.variables.append(block)
            csp.constraints[block] = []

        for j in csp.variables:
            if j.index == len(csp.variables) - 1:
                csp.constraints[j].append(Constraint([j], j.text + ' + ' + str(j.length) + ' < ' + firstLine[0]))
            else:
                if j.rowNumber == csp.variables[j.index + 1].rowNumber:

                    #j.text = 'b1'
                    #str(j.length) = '2'
                    #csp.variables[j.index + 1].text = 'b2'
                    #'b1 + 2 < b2'
                    csp.constraints[j].append(Constraint([j, csp.variables[j.index + 1]], j.text + ' + ' + str(j.length) + ' < ' + csp.variables[j.index + 1].text))
                else:
                    csp.constraints[j].append(Constraint([j], j.text + ' + ' + str(j.length) + ' < ' + firstLine[0]))

    return csp
csp = readCsp("scenario0")

for i in csp.constraints:
    for j in range(len(i)):
        print()




