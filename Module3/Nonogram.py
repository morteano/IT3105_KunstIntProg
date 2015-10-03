from graphics import *
from CSP import *
from Constraint import *
from copy import deepcopy
import heapq


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
            self.text = 'c' + str(self.col)
        else:
            self.text = 'r' + str(self.row)


class HeapQueue: #Priority queue with heap as data structure
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority): #adds element to the heap
        heapq.heappush(self.elements, (priority, item))

    def get(self): #returns the element with lowest value and removes it from the heap
        return heapq.heappop(self.elements)[1]


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


# Add domains to CSP
def addDomains(segmentCsp, rowCsp):
    # segment = 0
    # for row in range(numberOfRows):
    #     for seg in range(len(getVariablesInRow(segmentCsp, row))):
    #         for start in segmentCsp.domains[segmentCsp.variables[segment+seg]]:
    #             if seg == 0:
    #                 domainRow = [0]*numberOfColumns
    #             elif start - 1 == 1 or start - 2 == 1:
    #                 break
    #             for node in range(segmentCsp.variables[segment].length):
    #                 domainRow[start+node] = 1
    #         rowCsp.domains[rowCsp.variables[row]].append(domainRow)
    #         print(domainRow)
    #     segment += 1

    rows = [[0]*numberOfColumns]
    counter = 0
    for i in range(numberOfRows):
        domain = recursiveDomains(segmentCsp, rows, segmentCsp.variables[counter], 0, len(getVariablesInRow(segmentCsp, i)))
        for d in domain:
            rowCsp.domains[rowCsp.variables[i]].append(d)
        counter += len(getVariablesInRow(segmentCsp, i))

    columns = [[0]*numberOfRows]
    for i in range(numberOfRows, numberOfColumns+numberOfRows):
        domain = recursiveDomains(segmentCsp, columns, segmentCsp.variables[counter], 0, len(getVariablesInColumn(segmentCsp, i-numberOfRows)))
        for d in domain:
            rowCsp.domains[rowCsp.variables[i]].append(d)
        counter += len(getVariablesInColumn(segmentCsp, i-numberOfRows))


def recursiveDomains(csp, rows, var, segment, numberOfSegments):
    if segment == numberOfSegments:
        return rows
    domainResults = []
    for row in rows:
        lastNodeNr = -2
        for nodeNr in xrange(len(row)):
            if row[nodeNr] == 1:
                lastNodeNr = nodeNr
        for start in csp.domains[var]:
            tempRow = deepcopy(row)
            if segment != 0:
                if start > lastNodeNr+1 and var.rowNumber == csp.variables[var.index-1].rowNumber:
                    for node in range(var.length):
                        tempRow[start+node] = 1
                    domainResults.append(tempRow)
            else:
                for node in range(var.length):
                    tempRow[start+node] = 1
                domainResults.append(tempRow)

    if var.index == len(csp.variables)-1:
        nextVar = var
    else:
        nextVar = csp.variables[var.index+1]
    return recursiveDomains(csp, domainResults, nextVar, segment + 1, numberOfSegments)


def addConstraints(rowCsp):
    for row in range(numberOfRows):
        variable = rowCsp.variables[row]
        for col in range(numberOfColumns):
            rowCsp.constraints[variable].append(Constraint([variable, rowCsp.variables[numberOfRows+col]], variable.text + '[' + str(col) + ']' + ' == ' + rowCsp.variables[numberOfRows+col].text + '[' + str(row) + ']'))
            rowCsp.constraints[rowCsp.variables[numberOfRows+col]].append(Constraint([rowCsp.variables[numberOfRows+col], variable], variable.text + '[' + str(col) + ']' + ' == ' + rowCsp.variables[numberOfRows+col].text + '[' + str(row) + ']'))



def changeFromSegmentsToRows(segmentCsp):
    rowCsp = CSP()
    for row in range(numberOfRows):
        variable = LineSegment(row, -1)
        rowCsp.variables.append(variable)
        rowCsp.constraints[variable] = []
    for col in range(numberOfColumns):
        variable = LineSegment(-1, col)
        rowCsp.variables.append(variable)
        rowCsp.constraints[variable] = []

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

    return rowCsp


def heuristic(csp):
    value = len(csp.variables)
    for i in csp.variables:
        if len(csp.domains[i]) == 1:
            value -= 1
        if len(csp.domains[i]) == 0:
            value += len(csp.variables)
    return value


# Finds the smallest domain
def bestChoice(csp):
    domainSize = 10000000
    var = csp.variables[0]
    for i in csp.variables:
        if domainSize > len(csp.domains[i]) > 1:
            domainSize = len(csp.domains[i])
            var = i
    return var


def drawNonogram(csp):
    win = GraphWin("Nonogram", 600, 600)
    pixelSize = 600/max(numberOfColumns, numberOfRows)
    for row in xrange(numberOfRows):
        col = 0
        for node in csp.domains[csp.variables[row]][0]:
            rect = Rectangle(Point(pixelSize*col, 600-pixelSize*(row+1)), Point(pixelSize*col+pixelSize, 600-pixelSize*row))
            if node == 1:
                rect.setFill('blue')
            else:
                rect.setFill('white')
            rect.draw(win)
            col += 1
    win.getMouse()
    win.close()

def solveNonogram():
    # Find the segments in ech line
    segmentCsp = readCsp("scenario0")
    segmentCsp.initializeQueue()
    segmentCsp.domainFilter()

    # Make a cps where the segments from segmentCsp makes the domain
    lineCsp = changeFromSegmentsToRows(segmentCsp)
    lineCsp.initializeQueue()
    print("Before domainFilter:")
    for var in lineCsp.variables:
        print lineCsp.domains[var]
    lineCsp.domainFilter()
    print("After domainFilter:")
    for var in lineCsp.variables:
        print lineCsp.domains[var]

    openCsps = HeapQueue()

    openCsps.put(lineCsp, heuristic(lineCsp))

    numNodesInTree = 1

    numPoppedNodes = 0

    cameFrom = {}

    while not lineCsp.isSolved():
        lineCsp = openCsps.get()
        numPoppedNodes += 1

        # Find the next variable to guess on
        var = bestChoice(lineCsp)
        for i in range(len(lineCsp.domains[var])):
            nextCsp = deepcopy(lineCsp)

            nextVar = bestChoice(nextCsp)
            nextCsp.domains[nextVar] = [nextCsp.domains[nextVar][i]]
            nextCsp.progress += 1
            nextCsp.rerun(nextVar)
            nextCsp.domainFilter()

            numNodesInTree += 1

            cameFrom[nextCsp] = lineCsp
            openCsps.put(nextCsp, heuristic(nextCsp))

    return lineCsp


csp = solveNonogram()
#for var in csp.variables:
#    print(var.row, var.col, csp.domains[var])
drawNonogram(csp)