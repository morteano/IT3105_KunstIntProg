from random import randint
from graphics import *


colors = {1024:"red", 512:"orangered", 256:"darkorange", 128:"orange", 64:"gold", 32:"yellow", 16:"palegreen", 8:"yellowgreen", 4:"lawngreen", 2:"green", 0:"white"}

class Node:
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

        self.graphicRects = []

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
        node.color = colors[node.value]

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
        for j in range(self.size):
            for i in range(self.size):
                index = (i * self.size) + j
                if self.graphicRects[index][1] != self.nodes[j][i].color:
                    self.graphicRects[index][0].setFill(self.nodes[j][i].color)
                    self.graphicRects[index][1] = self.nodes[j][i].color
                    self.graphicRects[index][2].setText(self.nodes[j][i].value)

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



board = Board(4)
board.game()

