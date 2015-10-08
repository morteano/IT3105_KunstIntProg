from random import randint
from graphics import *
import heapq


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

class Node:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.value = 0


class Board:
    def __init__(self, size):
        self.size = size
        self.emptyNodes = []
        self.heap = HeapQueue()
        self.nodes = []
        for i in xrange(size):
            row = []
            for j in xrange(size):
                node = Node(i, j)
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
        node = self.emptyNodes.pop(randint(0, len(self.emptyNodes) - 1))
        if randint(0,9) < 9:
            node.value = 2
        else:
            node.value = 4

    def game(self):
        screenSize = 600
        win = GraphWin("2048", screenSize, screenSize)
        self.spawn()
        self.drawBoard(screenSize, win)
        while True:
            direction = raw_input("Press direction (WASD): ")
            self.move(direction)
            self.spawn()
            self.drawBoard(screenSize, win)
        win.getMouse()
        win.close()

    def drawBoard(self, screenSize, win):
        for j in range(self.size):
            for i in range(self.size):
                rect = Rectangle(Point(i*screenSize/self.size, j*screenSize/self.size),Point((i+1)*screenSize/self.size, (j+1)*screenSize/self.size))
                rect.setFill(colors[self.nodes[j][i].value])
                value = Text(Point((i+0.5)*screenSize/self.size, (j+0.5)*screenSize/self.size), self.nodes[j][i].value)
                rect.draw(win)
                if self.nodes[j][i].value != 0:
                    value.draw(win)

    def move(self, direction):
        if direction == 'a':
            self.moveLeft()
        elif direction == "d":
            self.moveRight()
        elif direction == "w":
            self.moveUp()
        elif direction == "s":
            self.moveDown()

    def moveLeft(self):
        for i in range(self.size):
            tempValue = 0
            index = 0
            for j in range(self.size):
                if tempValue != 0:
                    if tempValue == self.nodes[i][j].value:
                        tempNode.value *= 2
                        self.nodes[i][j].value = 0
                        self.emptyNodes.append(self.nodes[i][j])
                        tempValue = 0
                if self.nodes[i][j].value != 0:
                    tempValue = self.nodes[i][j].value
                    if j != index:
                        self.nodes[i][index].value = self.nodes[i][j].value
                        self.nodes[i][j].value = 0
                        self.emptyNodes.pop(self.emptyNodes.index(self.nodes[i][index]))
                        self.emptyNodes.append(self.nodes[i][j])
                    tempNode = self.nodes[i][index]
                    index += 1

    def moveRight(self):
        for i in range(self.size):
            tempValue = 0
            index = self.size - 1
            for j in range(self.size - 1, -1, -1):
                if tempValue != 0:
                    if tempValue == self.nodes[i][j].value:
                        tempNode.value *= 2
                        self.nodes[i][j].value = 0
                        self.emptyNodes.append(self.nodes[i][j])
                        tempValue = 0
                if self.nodes[i][j].value != 0:
                    tempValue = self.nodes[i][j].value
                    if j != index:
                        self.nodes[i][index].value = self.nodes[i][j].value
                        self.nodes[i][j].value = 0
                        self.emptyNodes.pop(self.emptyNodes.index(self.nodes[i][index]))
                        self.emptyNodes.append(self.nodes[i][j])
                    tempNode = self.nodes[i][index]
                    index -= 1

    def moveUp(self):
        for i in range(self.size):
            tempValue = 0
            index = 0
            for j in range(self.size):
                if tempValue != 0:
                    if tempValue == self.nodes[j][i].value:
                        tempNode.value *= 2
                        self.nodes[j][i].value = 0
                        self.emptyNodes.append(self.nodes[j][i])
                        tempValue = 0
                if self.nodes[j][i].value != 0:
                    tempValue = self.nodes[j][i].value
                    if j != index:
                        self.nodes[index][i].value = self.nodes[j][i].value
                        self.nodes[j][i].value = 0
                        self.emptyNodes.pop(self.emptyNodes.index(self.nodes[index][i]))
                        self.emptyNodes.append(self.nodes[j][i])
                    tempNode = self.nodes[index][i]
                    index += 1

    def moveDown(self):
        for i in range(self.size):
            tempValue = 0
            index = self.size - 1
            for j in range(self.size - 1, -1, -1):
                if tempValue != 0:
                    if tempValue == self.nodes[j][i].value:
                        tempNode.value *= 2
                        self.nodes[j][i].value = 0
                        self.emptyNodes.append(self.nodes[j][i])
                        tempValue = 0
                if self.nodes[j][i].value != 0:
                    tempValue = self.nodes[j][i].value
                    if j != index:
                        self.nodes[index][i].value = self.nodes[j][i].value
                        self.nodes[j][i].value = 0
                        self.emptyNodes.pop(self.emptyNodes.index(self.nodes[index][i]))
                        self.emptyNodes.append(self.nodes[j][i])
                    tempNode = self.nodes[index][i]
                    index -= 1

    def findChildren(self):
        # Find children
        return

    def addChildren(self):
        self.findChildren()
        self.heap()


    def solver(self):
        screenSize = 600
        win = GraphWin("2048", screenSize, screenSize)
        self.drawBoard(screenSize, win)
        while len(self.emptyNodes) > 0:
            self.addChildren()
            self.nodes = self.heap.get()
            self.updateBoard





board = Board(4)
board.nodes[0][0].value = 8192
board.nodes[0][1].value = 4096
board.nodes[0][2].value = 2048
board.nodes[0][3].value = 1024
board.nodes[1][0].value = 512
board.nodes[1][1].value = 256
board.nodes[1][2].value = 128
board.nodes[1][3].value = 64
board.nodes[2][0].value = 32
board.nodes[2][1].value = 16
board.nodes[2][2].value = 8
board.nodes[2][3].value = 4

win = GraphWin("2048", 600,600)
board.drawBoard(600, win)
win.getMouse()

