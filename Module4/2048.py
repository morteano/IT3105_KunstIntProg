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
        for i in range(self.size):
            tempValue = 0
            index = 0
            for j in range(self.size):
                if tempValue != 0:
                    if tempValue == self.nodes[i][j].value:
                        tempNode.value *= 2
                        self.nodes[i][j].value = 0
                        tempValue = 0
                if self.nodes[i][j].value != 0:
                    tempValue = self.nodes[i][j].value
                    if j != index:
                        self.nodes[i][index].value = self.nodes[i][j].value
                        self.nodes[i][j].value = 0
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
                        tempValue = 0
                if self.nodes[i][j].value != 0:
                    tempValue = self.nodes[i][j].value
                    if j != index:
                        self.nodes[i][index].value = self.nodes[i][j].value
                        self.nodes[i][j].value = 0
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
                        tempValue = 0
                if self.nodes[j][i].value != 0:
                    tempValue = self.nodes[j][i].value
                    if j != index:
                        self.nodes[index][i].value = self.nodes[j][i].value
                        self.nodes[j][i].value = 0
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
                        tempValue = 0
                if self.nodes[j][i].value != 0:
                    tempValue = self.nodes[j][i].value
                    if j != index:
                        self.nodes[index][i].value = self.nodes[j][i].value
                        self.nodes[j][i].value = 0
                    tempNode = self.nodes[index][i]
                    index -= 1



board = Board(4)
board.printBoard()
#board.spawn()
board.setValue(0, 3, 8)
board.setValue(0, 2, 2)
board.setValue(0, 1, 2)
board.setValue(0, 0, 2)
board.setValue(3, 3, 16)
board.setValue(2, 3, 16)
board.setValue(2, 1, 2)

print("")
board.printBoard()
board.moveDown()
print("")
board.printBoard()

