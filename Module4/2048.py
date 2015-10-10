from random import randint
from graphics import *
import heapq
import time
from copy import deepcopy

from Tree import *

colors = {8192:"Navy", 4096:"Midnightblue", 2048:"darkred", 1024:"red", 512:"orangered", 256:"darkorange", 128:"orange", 64:"gold", 32:"yellow", 16:"palegreen", 8:"yellowgreen", 4:"lawngreen", 2:"green", 0:"white"}
graphRect = []


class HeapQueue: #Priority queue with heap as data structure
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority): #adds element to the heap
        heapq.heappush(self.elements, (priority, item))

    def get(self): #returns the element with lowest value and removes it from the heap
        return heapq.heappop(self.elements)[1]

class Tile:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.value = 0
        self.color = colors[self.value]


class Board:
    def __init__(self, size):
        self.size = size
        self.emptyNodes = []
        self.nodes = []

        self.children = []
        self.parent = None

        self.heuristic = 0

        self.graphicRects = []

        self.cameFrom = "qwerty"

        for i in xrange(size):
            row = []
            for j in xrange(size):
                node = Tile(i, j)
                row.append(node)
                self.emptyNodes.append(node)
            self.nodes.append(row)

    def printBoard(self):
        for i in xrange(self.size):
            row = []
            for j in xrange(self.size):
                row.append(self.nodes[i][j].value)
            print(row)

    def setValue(self, x, y, value):
        self.nodes[x][y].value = value

    def spawn(self):
        random = randint(0, len(self.emptyNodes) - 1)
        node = self.emptyNodes.pop(random)
        if randint(0,9) < 9:
            node.value = 2
        else:
            node.value = 4
        node.color = colors[node.value]

        return random, node.value

    def game(self):
        screenSize = 600
        win = GraphWin("2048", screenSize, screenSize)
        self.spawn()
        self.drawBoard(screenSize, win)
        while True:
            direction = raw_input("Press direction (WASD): ")
            self.move(direction)
            self.spawn()
            self.updateBoard()
        win.getMouse()
        win.close()

    def drawBoard(self, screenSize, win):
        for j in range(self.size):
            for i in range(self.size):
                rect = Rectangle(Point(i*screenSize/self.size, j*screenSize/self.size),Point((i+1)*screenSize/self.size, (j+1)*screenSize/self.size))
                rect.setFill(self.nodes[j][i].color)
                rect.setFill(colors[self.nodes[j][i].value])
                value = Text(Point((i+0.5)*screenSize/self.size, (j+0.5)*screenSize/self.size), self.nodes[j][i].value)
                self.graphicRects.append([rect, self.nodes[j][i].color, value])
                rect.draw(win)
                #if self.nodes[j][i].value != 0:
                value.draw(win)



    def updateBoard(self):
        change = False
        for j in range(self.size):
            for i in range(self.size):
                index = (j * self.size) + i
                if self.graphicRects[index][1] != self.nodes[j][i].color:
                    self.graphicRects[index][0].setFill(self.nodes[j][i].color)
                    self.graphicRects[index][1] = self.nodes[j][i].color
                    self.graphicRects[index][2].setText(self.nodes[j][i].value)
                    change = True
        return change

    def move(self, direction):
        if direction == 'a':
            self.moveLeft()
        elif direction == "d":
            self.moveRight()
        elif direction == "w":
            self.moveUp()
        elif direction == "s":
            self.moveDown()
        self.cameFrom = direction

    def moveLeft(self):
        for i in range(self.size):
            tempValue = 0
            index = 0
            for j in range(self.size):
                if tempValue != 0:
                    if tempValue == self.nodes[i][j].value:
                        tempNode.value *= 2
                        tempNode.color = colors[tempNode.value]
                        self.nodes[i][j].value = 0
                        self.nodes[i][j].color = colors[self.nodes[i][j].value]
                        self.emptyNodes.append(self.nodes[i][j])
                        tempValue = 0
                if self.nodes[i][j].value != 0:
                    tempValue = self.nodes[i][j].value
                    if j != index:
                        self.nodes[i][index].value = self.nodes[i][j].value
                        self.nodes[i][index].color = colors[self.nodes[i][index].value]
                        self.nodes[i][j].value = 0
                        self.nodes[i][j].color = colors[self.nodes[i][j].value]
                        self.emptyNodes.pop(self.emptyNodes.index(self.nodes[i][index]))
                        self.emptyNodes.append(self.nodes[i][j])
                    tempNode = self.nodes[i][index]
                    index += 1
        return self

    def moveRight(self):
        for i in range(self.size):
            tempValue = 0
            index = self.size - 1
            for j in range(self.size - 1, -1, -1):
                if tempValue != 0:
                    if tempValue == self.nodes[i][j].value:
                        tempNode.value *= 2
                        tempNode.color = colors[tempNode.value]
                        self.nodes[i][j].value = 0
                        self.nodes[i][j].color = colors[self.nodes[i][j].value]
                        self.emptyNodes.append(self.nodes[i][j])
                        tempValue = 0
                if self.nodes[i][j].value != 0:
                    tempValue = self.nodes[i][j].value
                    if j != index:
                        self.nodes[i][index].value = self.nodes[i][j].value
                        self.nodes[i][index].color = colors[self.nodes[i][index].value]
                        self.nodes[i][j].value = 0
                        self.nodes[i][j].color = colors[self.nodes[i][j].value]
                        self.emptyNodes.pop(self.emptyNodes.index(self.nodes[i][index]))
                        self.emptyNodes.append(self.nodes[i][j])
                    tempNode = self.nodes[i][index]
                    index -= 1
        return self

    def moveUp(self):
        for i in range(self.size):
            tempValue = 0
            index = 0
            for j in range(self.size):
                if tempValue != 0:
                    if tempValue == self.nodes[j][i].value:
                        tempNode.value *= 2
                        tempNode.color = colors[tempNode.value]
                        self.nodes[j][i].value = 0
                        self.nodes[j][i].color = colors[self.nodes[j][i].value]
                        self.emptyNodes.append(self.nodes[j][i])
                        tempValue = 0
                if self.nodes[j][i].value != 0:
                    tempValue = self.nodes[j][i].value
                    if j != index:
                        self.nodes[index][i].value = self.nodes[j][i].value
                        self.nodes[index][i].color = colors[self.nodes[index][i].value]
                        self.nodes[j][i].value = 0
                        self.nodes[j][i].color = colors[self.nodes[j][i].value]
                        self.emptyNodes.pop(self.emptyNodes.index(self.nodes[index][i]))
                        self.emptyNodes.append(self.nodes[j][i])
                    tempNode = self.nodes[index][i]
                    index += 1
        return self

    def moveDown(self):
        for i in range(self.size):
            tempValue = 0
            index = self.size - 1
            for j in range(self.size - 1, -1, -1):
                if tempValue != 0:
                    if tempValue == self.nodes[j][i].value:
                        tempNode.value *= 2
                        tempNode.color = colors[tempNode.value]
                        self.nodes[j][i].value = 0
                        self.nodes[j][i].color = colors[self.nodes[j][i].value]
                        self.emptyNodes.append(self.nodes[j][i])
                        tempValue = 0
                if self.nodes[j][i].value != 0:
                    tempValue = self.nodes[j][i].value
                    if j != index:
                        self.nodes[index][i].value = self.nodes[j][i].value
                        self.nodes[index][i].color = colors[self.nodes[index][i].value]
                        self.nodes[j][i].value = 0
                        self.nodes[j][i].color = colors[self.nodes[j][i].value]
                        self.emptyNodes.pop(self.emptyNodes.index(self.nodes[index][i]))
                        self.emptyNodes.append(self.nodes[j][i])
                    tempNode = self.nodes[index][i]
                    index -= 1
        return self

def legalMoves(board):
    movable = False
    for i in xrange(board.size-1):
        for j in xrange(board.size):
            if board.nodes[i][j].value == board.nodes[i+1][j].value:
                movable = True
    for i in xrange(board.size):
        for j in xrange(board.size-1):
            if board.nodes[i][j].value == board.nodes[i][j+1].value:
                movable = True
    return movable

def createAllPossibleBoards(board):
    list = []
    for i in board.emptyNodes:
        child1 = deepcopy(board)
        node1 = child1.nodes[i.xPos][i.yPos]
        node1.value = 2
        child1.emptyNodes.pop(child1.emptyNodes.index(node1))
        child2 = deepcopy(board)
        node2 = child2.nodes[i.xPos][i.yPos]
        node2.value = 4
        child2.emptyNodes.pop(child2.emptyNodes.index(node2))
        list.append(child1)
        list.append(child2)

    return list


def createTree(tree, depth, root):
    if depth == 0:
        return tree

    for i in ["a", "d", "w", "s"]:
        board = deepcopy(root)
        board.move(i)
        tree.addNode(board, root)

    for i in tree.root.children:
        children = createAllPossibleBoards(i)

        for j in children:
            tree.addNode(j, i)
            return createTree(tree, depth - 2, j)

def addToTree(tree, depth, root, extraDepth):
    if depth == 0:
        createTree(tree, extraDepth, root)
    for i in root.children:
        for j in i.children:
            addToTree(tree, depth - 2, j, extraDepth - 2)

def minimax(tree, depth, root):
    maxHeuristic = 0
    dir = ""
    for i in root.children:
        heurI = findHeuristic(tree, depth, i)
        if  heurI > maxHeuristic:
            maxHeuristic = heurI
            dir = i.cameFrom
    return dir

def findHeuristic(tree, depth, root):
    if depth == 0:
        return heuristic(root)
    elif depth%2 == 1:
        heur = 0
        for i in root.children:
            it = 0
            if it%2 == 0:
                prob = 0.9
            else:
                prob = 0.1
            it += 1
            heur += findHeuristic(tree, depth-1, i)*prob
        return heur
    else:
        for i in root.children:
            return findHeuristic(tree, depth-1, i)


def heuristic(board):
    return 16-len(board.emptyNodes)


def solver(board):
    #screenSize = 600
    #win = GraphWin("2048", screenSize, screenSize)
    #board.drawBoard(screenSize, win)
    currentBoard = board

    heap = HeapQueue()

    depth = 2

    tree = Tree()
    tree.addNode(currentBoard, None)
    createTree(tree, depth, currentBoard)
    tree.depth = depth
    while True:
        if len(currentBoard.emptyNodes) <= 0:
            if not legalMoves(currentBoard):
                break
        currentBoard.move(minimax(tree, depth, currentBoard))

        if currentBoard.cameFrom == "a":
            currentChild = currentBoard.children[0]
        elif currentBoard.cameFrom == "d":
            currentChild = currentBoard.children[1]
        elif currentBoard.cameFrom == "w":
            currentChild = currentBoard.children[2]
        else:
            currentChild = currentBoard.children[3]

        childIndex, value = currentChild.spawn()

        print(len(currentChild.children))
        print((childIndex * 2) + (value / 2) - 1)
        root = currentChild.children[(childIndex * 2) + (value / 2) - 1]

        tree.depth -= 2
        extraDepth = 2
        addToTree(tree, tree.depth, root, extraDepth)
        tree.depth += extraDepth

        currentBoard = deepcopy(root)
        currentBoard.printBoard()
        print("")
        time.sleep(1)

    #win.getMouse()
    #win.close()


"""def dummySolve():
    screenSize = 600
    win = GraphWin("2048", screenSize, screenSize)
    self.spawn()
    self.drawBoard(screenSize, win)
    counter = 0
    while True:
        if counter%2 == 0:
            self.move('s')
        elif counter%101 == 0:
            self.move('d')
        else:
            self.move('a')
        if self.updateBoard():
            self.spawn()
        counter += 1
        time.sleep(0.05)
    win.getMouse()"""

board = Board(4)
#board.game()
solver(board)
