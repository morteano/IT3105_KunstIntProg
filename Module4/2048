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

    def spawn(self):
        node = self.emptyNodes.pop(randint(0, len(self.emptyNodes)))
        if randint(0,9) < 9:
            node.value = 2
        else:
            node.value = 4

board = Board(4)
board.printBoard()
board.spawn()
print("")
board.printBoard()
