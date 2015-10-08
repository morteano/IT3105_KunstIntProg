from random import randint


class Node:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.value = 0


class Board:
    def __init__(self, size):
        self.size = size
        self.emptyNodes = []
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
        node = self.emptyNodes.pop(randint(0, len(self.emptyNodes)))
        if randint(0,9) < 9:
            node.value = 2
        else:
            node.value = 4

    def moveLeft(self):
        tempValue = 0
        for i in range(self.size):
            for j in range(self.size):
                if tempValue != 0:
                    if tempValue == self.nodes[i][j].value:
                        tempNode.value *= 2
                        self.nodes[i][j].value = 0
                if self.nodes[i][j].value != 0:
                    if tempValue == 0:
                        tempValue = self.nodes[i][j].value
                        self.nodes[i][0].value = self.nodes[i][j].value
                        self.nodes[i][j].value = 0
                        tempNode = self.nodes[i][0]
                    else:
                        tempValue = self.nodes[i][j].value
                        tempNode = self.nodes[i][j]



board = Board(4)
board.printBoard()
#board.spawn()
board.setValue(0, 3, 2)
board.setValue(0, 0, 2)
print("")
board.printBoard()
board.moveLeft()
print("")
board.printBoard()

