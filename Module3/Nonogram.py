from graphics import *

from CSP import *
from Constraint import *
from copy import deepcopy


class Node:

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.filled = False


class Block:
    # Segments in row or column
    def __init__(self, index, length, rowNumber, colNumber):
        self.index = index
        self.rowNumber = rowNumber
        self.colNumber = colNumber
        self.length = length
        if self.rowNumber == -1:
            self.text = 'cb' + str(self.index)
        else:
            self.text = 'rb' + str(self.index)


class LineSegment:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        if self.row == -1:
            self.text = 'c' + str(self.row)
        else:
            self.text = 'r' + str(self.row)

# Global variables
numberOfRows = 0
numberOfColumns = 0

def readCsp(textFile):
    csp = CSP()

    board = []

    file = open(textFile)

    firstLine = file.readline().split(" ")
    global numberOfRows
    numberOfRows = int(firstLine[1])
    global numberOfColumns
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
            block = Block(counter, int(j), i, -1)
            counter += 1
            csp.variables.append(block)
            csp.constraints[block] = []
            csp.domains[block] = deepcopy(domainX)

    # Add start position for segments in columns
    for i in range(numberOfColumns):
        line = file.readline().split(" ")
        for j in line:
            block = Block(counter, int(j), -1, i)
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
        elif j.colNumber == -1:
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
            if j.colNumber == csp.variables[j.index + 1].colNumber:
                csp.constraints[j].append(Constraint([j, csp.variables[j.index + 1]], j.text + ' + ' + str(j.length) + ' < ' + csp.variables[j.index + 1].text))
                csp.constraints[csp.variables[j.index + 1]].append(Constraint([csp.variables[j.index + 1], j], j.text + ' + ' + str(j.length) + ' < ' + csp.variables[j.index + 1].text))
            else:
                csp.constraints[j].append(Constraint([j], j.text + ' + ' + str(j.length) + ' <= ' + str(numberOfRows)))

    return csp

def getVariablesInRow(csp, row):
    list = []
    for i in csp.variables:
        if i.rowNumber != -1:
            if i.rowNumber == row:
                list.append(i)
    return list

def getVariablesInColumn(csp, col):
    list = []
    for i in csp.variables:
        if i.colNumber != -1:
            if i.colNumber == col:
                list.append(i)
    return list


def remove(row, columns, elementNrRow, elementNrCol):
    remove = True
    for col in columns:
        if col[elementNrCol] == row[elementNrRow]:
            remove = False
            break
    return remove


# TODO: Find out som genius way to do this
# Add domains to CSP
def addDomains(segmentCsp, rowCsp):
    segment = 0
    for row in range(numberOfRows):
        print row
        print(segmentCsp.domains[segmentCsp.variables[segment]])
        for start in segmentCsp.domains[segmentCsp.variables[segment]]:
            for seg in range(len(getVariablesInRow(segmentCsp, row))):
                if seg == 0:
                    domainRow = [0]*numberOfColumns
                elif start - 1 == 1 or start - 2 == 1:
                    break
                for node in range(segmentCsp.variables[segment].length):
                    print(start+node)
                    domainRow[start+node] = 1
            rowCsp.domains[rowCsp.variables[row]].append(domainRow)
        segment += 1


# TODO: Do some more magic!
def addConstraints(rowCsp):
    for row in range(numberOfRows):
        var = rowCsp.variables[row]
        for col in range(numberOfColumns):
            rowCsp.constraints[var].append(Constraint([var, csp.variables[numberOfRows+col]], var.text + '[' + str(col) + ']' + ' = ' + csp.variables[numberOfRows+col].text + '[' + str(row) + ']'))



def changeFromSegmentsToRows(segmentCsp):
    rowCsp = CSP()
    for row in range(numberOfRows):
        rowCsp.variables.append(LineSegment(row, -1))
    for col in range(numberOfColumns):
        rowCsp.variables.append(LineSegment(-1, col))

    # Add rows as variables to CSP
    for row in range(numberOfRows):
        rowCsp.domains[rowCsp.variables[row]] = []

    # Add columns as variables to CSP
    for col in range(numberOfColumns):
        rowCsp.domains[rowCsp.variables[numberOfRows+col]] = []

    # Add domain to rowCsp
    addDomains(segmentCsp, rowCsp)

    # Add constraints to rowCsp
    addConstraints(rowCsp)





csp = readCsp("scenario0")
# for i in csp.variables:
#     for j in csp.constraints[i]:
#         print(j.expression)
#
# for i in csp.variables:
#     print(csp.domains[i])
csp.initializeQueue()
csp.domainFilter()
# print("\n")
# for i in csp.variables:
#     print(i.text, csp.domains[i])
changeFromSegmentsToRows(csp)

