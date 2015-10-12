from random import randint
from graphics import *
import heapq
import time
from copy import deepcopy
from visuals import GameWindow

from Tree import *

boardSize = 4
board = [0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0]


def printBoard(board):
    for i in xrange(boardSize):
        row = []
        for j in xrange(boardSize):
            row.append(board[boardSize*i+j])
        print(row)

# Spawns a tile with 0.9 prob of being 2, 0.1 prob of being 4 in an empty tile
def spawn(board):
    emptyNodes = []
    for i in range(len(board)):
        if board[i] == 0:
            emptyNodes.append(i)
    random = randint(0, len(emptyNodes) - 1)
    if randint(0,9) < 9:
        board[emptyNodes[random]] = 2
    else:
        board[emptyNodes[random]] = 4
    return board

def move(board, direction):
    if direction == 'a':
        board = moveLeft(board)
    elif direction == "d":
        board = moveRight(board)
    elif direction == "w":
        board = moveUp(board)
    elif direction == "s":
        board = moveDown(board)
    return board


def moveLeft(board):
    for i in range(boardSize):
        tempValue = 0
        index = 0
        for j in range(boardSize):
            if tempValue != 0:
                if tempValue == board[boardSize*i+j]:
                    board[tempNodeIndex] *= 2
                    board[boardSize*i+j] = 0
                    tempValue = 0
            if board[boardSize*i+j] != 0:
                tempValue = board[boardSize*i+j]
                if j != index:
                    board[boardSize*i+index] = board[boardSize*i+j]
                    board[boardSize*i+j] = 0
                tempNodeIndex = boardSize*i+index
                index += 1
    return board


def moveRight(board):
    for i in range(boardSize):
        tempValue = 0
        index = boardSize - 1
        for j in range(boardSize - 1, -1, -1):
            if tempValue != 0:
                if tempValue == board[boardSize*i+j]:
                    board[tempNodeIndex] *= 2
                    board[boardSize*i+j] = 0
                    tempValue = 0
            if board[boardSize*i+j] != 0:
                tempValue = board[boardSize*i+j]
                if j != index:
                    board[boardSize*i+index] = board[boardSize*i+j]
                    board[boardSize*i+j] = 0
                tempNodeIndex = boardSize*i+index
                index -= 1
    return board


def moveUp(board):
    for i in range(boardSize):
        tempValue = 0
        index = 0
        for j in range(boardSize):
            if tempValue != 0:
                if tempValue == board[boardSize*j+i]:
                    board[tempNodeIndex] *= 2
                    board[boardSize*j+i] = 0
                    tempValue = 0
            if board[boardSize*j+i] != 0:
                tempValue = board[boardSize*j+i]
                if j != index:
                    board[boardSize*index+i] = board[boardSize*j+i]
                    board[boardSize*j+i] = 0
                tempNodeIndex = boardSize*index+i
                index += 1
    return board

def moveDown(board):
    for i in range(boardSize):
        tempValue = 0
        index = boardSize - 1
        for j in range(boardSize - 1, -1, -1):
            if tempValue != 0:
                if tempValue == board[boardSize*j+i]:
                    board[tempNodeIndex] *= 2
                    board[boardSize*j+i] = 0
                    tempValue = 0
            if board[boardSize*j+i] != 0:
                tempValue = board[boardSize*j+i]
                if j != index:
                    board[boardSize*index+i] = board[boardSize*j+i]
                    board[boardSize*j+i] = 0
                tempNodeIndex = boardSize*index+i
                index -= 1
    return board

def game(board):
        window = GameWindow( )
        board = spawn(board)
        printBoard(board)
        while True:
            direction = raw_input("Press direction (WASD): ")
            board = move(board, direction)
            board = spawn(board)
            printBoard(board)
            window.update_view(board)


def legalMoves(board):
    movable = False
    for i in xrange(boardSize-1):
        for j in xrange(boardSize):
            if board[boardSize*i+j] == board[boardSize*(i+1)+j]:
                movable = True
    for i in xrange(boardSize):
        for j in xrange(boardSize-1):
            if board[boardSize*i+j] == board[boardSize*i+j+1]:
                movable = True
    return movable



# class Board:
#     def __init__(self, size):
#         self.size = size
#         self.emptyNodes = []
#         self.nodes = []
#
#         self.children = []
#         self.parent = None
#
#         self.heuristic = 0
#
#         self.graphicRects = []
#
#         self.cameFrom = "qwerty"
#
#         for i in xrange(size):
#             row = []
#             for j in xrange(size):
#                 node = Tile(i, j)
#                 row.append(node)
#                 self.emptyNodes.append(node)
#             self.nodes.append(row)
#
#
#     def drawBoard(self, screenSize, win):
#         for j in range(self.size):
#             for i in range(self.size):
#                 rect = Rectangle(Point(i*screenSize/self.size, j*screenSize/self.size),Point((i+1)*screenSize/self.size, (j+1)*screenSize/self.size))
#                 rect.setFill(self.nodes[j][i].color)
#                 rect.setFill(colors[self.nodes[j][i].value])
#                 value = Text(Point((i+0.5)*screenSize/self.size, (j+0.5)*screenSize/self.size), self.nodes[j][i].value)
#                 self.graphicRects.append([rect, self.nodes[j][i].color, value])
#                 rect.draw(win)
#                 #if self.nodes[j][i].value != 0:
#                 value.draw(win)
#
#
#
#     def updateBoard(self):
#         change = False
#         for j in range(self.size):
#             for i in range(self.size):
#                 index = (j * self.size) + i
#                 if self.graphicRects[index][1] != self.nodes[j][i].color:
#                     self.graphicRects[index][0].setFill(self.nodes[j][i].color)
#                     self.graphicRects[index][1] = self.nodes[j][i].color
#                     self.graphicRects[index][2].setText(self.nodes[j][i].value)
#                     change = True
#         return change
#
#
#
# def createAllPossibleBoards(board):
#     list = []
#     for i in board.emptyNodes:
#         child1 = deepcopy(board)
#         node1 = child1.nodes[i.xPos][i.yPos]
#         node1.value = 2
#         child1.emptyNodes.pop(child1.emptyNodes.index(node1))
#         child2 = deepcopy(board)
#         node2 = child2.nodes[i.xPos][i.yPos]
#         node2.value = 4
#         child2.emptyNodes.pop(child2.emptyNodes.index(node2))
#         list.append(child1)
#         list.append(child2)
#
#     return list
#
#
# def createTree(tree, depth, root):
#     if depth == 0:
#         return tree
#
#     for i in ["a", "d", "w", "s"]:
#         board = deepcopy(root)
#         board.move(i)
#         tree.addNode(board, root)
#
#     for i in tree.root.children:
#         children = createAllPossibleBoards(i)
#
#         for j in children:
#             tree.addNode(j, i)
#             createTree(tree, depth - 2, j)
#
# def addToTree(tree, depth, root, extraDepth):
#     if depth == 0:
#         print("Start")
#         createTree(tree, extraDepth, root)
#         print("End")
#     for i in root.children:
#         for j in i.children:
#             addToTree(tree, depth - 2, j, extraDepth - 2)
#
# def minimax(tree, depth, root):
#     maxHeuristic = 0
#     dir = ""
#     for i in root.children:
#         heurI = findHeuristic(tree, depth, i)
#         if  heurI > maxHeuristic:
#             maxHeuristic = heurI
#             dir = i.cameFrom
#     return dir
#
# def findHeuristic(tree, depth, root):
#     if depth == 0:
#         return heuristic(root)
#     elif depth%2 == 1:
#         heur = 0
#         for i in root.children:
#             it = 0
#             if it%2 == 0:
#                 prob = 0.9
#             else:
#                 prob = 0.1
#             it += 1
#             heur += findHeuristic(tree, depth-1, i)*prob
#         return heur
#     else:
#         for i in root.children:
#             return findHeuristic(tree, depth-1, i)
#
#
# def heuristic(board):
#     return 16-len(board.emptyNodes)
#
#
# def solver(board):
#     #screenSize = 600
#     #win = GraphWin("2048", screenSize, screenSize)
#     #board.drawBoard(screenSize, win)
#     currentBoard = board
#
#     heap = HeapQueue()
#
#     depth = 2
#
#     tree = Tree()
#     tree.addNode(currentBoard, None)
#     createTree(tree, depth, currentBoard)
#     tree.depth = depth
#     while True:
#         if len(currentBoard.emptyNodes) <= 0:
#             if not legalMoves(currentBoard):
#                 break
#         currentBoard.move(minimax(tree, depth, currentBoard))
#
#         if currentBoard.cameFrom == "a":
#             currentChild = currentBoard.children[0]
#         elif currentBoard.cameFrom == "d":
#             currentChild = currentBoard.children[1]
#         elif currentBoard.cameFrom == "w":
#             currentChild = currentBoard.children[2]
#         else:
#             currentChild = currentBoard.children[3]
#
#         childIndex, value = currentChild.spawn()
#         print("1")
#         root = currentChild.children[(childIndex * 2) + (value / 2) - 1]
#         tree.depth -= 2
#         extraDepth = 2
#         print("2")
#         #addToTree(tree, tree.depth, root, extraDepth)
#         tree.reset()
#         tree.addNode(root, None)
#         print("Start")
#         createTree(tree, depth, root)
#         print("End")
#         tree.depth += extraDepth
#         print("3")
#         currentBoard = deepcopy(root)
#         currentBoard.printBoard()
#         print("")
#         time.sleep(1)
#
#     #win.getMouse()
#     #win.close()
#
#
# """def dummySolve():
#     screenSize = 600
#     win = GraphWin("2048", screenSize, screenSize)
#     self.spawn()
#     self.drawBoard(screenSize, win)
#     counter = 0
#     while True:
#         if counter%2 == 0:
#             self.move('s')
#         elif counter%101 == 0:
#             self.move('d')
#         else:
#             self.move('a')
#         if self.updateBoard():
#             self.spawn()
#         counter += 1
#         time.sleep(0.05)
#     win.getMouse()"""
#
# #board.game()
# #solver(board)
# window = GameWindow( )
# board = [   # A list of values currently present in the board on the form 2^x.
#             # Eg: the number 4 implies that the graphical board should display,
#             # 2^4 = 16, the digit 16. This board represents the board in the screen dump below.
#             0, 2, 4, 4,
#             0, 2, 1, 3,
#             0, 1, 1, 3,
#             0, 0, 2, 1
#         ]

# window.update_view( board ) # 1D list representing the board
# adls = raw_input("dskgs")
# board = [0,0,2,2,
#          0,2,0,2,
#          2,0,2,0,
#          2,0,4,2,]

game(board)
