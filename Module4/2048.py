from random import randint, random, choice
from graphics import *
import heapq
import time
from copy import deepcopy
from visuals import GameWindow
from Tree import *
from GUI import *


class Node:
    def __init__(self, board, parent, lastMove):
        self.board = board
        self.parent = parent
        self.lastMove = lastMove
        self.children = []

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
    print(" ")

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
    return board, random, board[emptyNodes[random]]


def move(board, direction):
    oldBoard = list(board)
    modified = False
    if direction == 'a':
        board = moveLeft(board)
    elif direction == "d":
        board = moveRight(board)
    elif direction == "w":
        board = moveUp(board)
    elif direction == "s":
        board = moveDown(board)
    if oldBoard != board:
        modified = True
    return board, modified


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
        # window = GameWindow( )
        board = spawn(board)
        gui = getNewBoardWindow(4, None)
        while True:
            direction = raw_input("Press direction (WASD): ")
            board = move(board, direction)
            board = spawn(board)
            time.sleep(0.5)
            # window.update_view(board)

            gui.drawBoard(board)


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


def addToTree(tree, depth, root, extraDepth):
    if depth == 0:
        createTree(tree, extraDepth, root)
    for i in root.children:
        for j in i.children:
            addToTree(tree, depth - 2, j, extraDepth - 2)


def createTree(tree, depth, root):
    if depth == 0:
        return tree
    for i in ["a", "d", "w", "s"]:
        board = list(root.board)
        board, modified = move(board, i)
        if modified:
            tree.addNode(Node(board, root, i), root)

    for i in tree.root.children:
        children = createAllPossibleBoards(i)

        for j in children:
            tree.addNode(j, i)
            tree = createTree(tree, depth - 2, j)
    return tree

def createAllPossibleBoards(node):
    emptyNodes = []
    for i in range(len(node.board)):
        if node.board[i] == 0:
            emptyNodes.append(i)
    nodeList = []
    for i in emptyNodes:
        child1 = Node(list(node.board), node, node.lastMove)
        child1.board[i] = 2
        child2 = Node(list(node.board), node, node.lastMove)
        child2.board[i] = 4
        nodeList.append(child1)
        nodeList.append(child2)
    return nodeList


def minimax(tree, depth, root):
    maxHeuristic = -1
    dir = ""
    bestIndex = 0
    index = 0
    print len(root.children)
    for i in root.children:
        heurI = findHeuristic(depth-1, i, 0)
        if  heurI > maxHeuristic:
            maxHeuristic = heurI
            dir = i.lastMove
            bestIndex = index
        index += 1
    print(dir)
    return dir, bestIndex

def findHeuristic(depth, root, heur):
    if depth == 0:
        return heur + heuristic(root.board)
    elif depth % 2 == 1:
        for i in root.children:
            it = 0
            if it%2 == 0:
                prob = 0.9
            else:
                prob = 0.1
            it += 1
            heur += (findHeuristic(depth-1, i, heur)*prob)/len(root.children)
        return heur
    else:
        for i in root.children:
            heur += findHeuristic(depth-1, i, heur)/len(root.children)
        return heur

def heuristic(board):
    empty = 0
    for i in range(len(board)):
        if board[i] == 0:
            empty += 1
    return empty

def solver(board):
    board, random, value = spawn(board)
    gui = getNewBoardWindow(4, None)
    depth = 2

    tree = Tree()
    node = Node(board, None, None)
    tree.addNode(node, None)
    tree = createTree(tree, depth, node)
    tree.depth = depth
    full = False
    while True:
        empty = 0
        for tile in board:
            if tile == 0:
                empty += 1
        if empty == 0:
            print("full board")
            if not legalMoves(board):
                print("Trying to break")
                break
        dir, index = minimax(tree, depth, node)
        printBoard(board)
        print dir
        board, modified = move(board, dir)
        board, childIndex, value = spawn(board)
        if dir == "a":
            child = 0
        elif dir == "d":
            child = 1
        elif dir == "w":
            child = 2
        elif dir == "s":
            child = 3
        else:
            print("Error....")
        print (childIndex * 2) + (value / 2) - 1
        node = node.children[index].children[(childIndex * 2) + (value / 2) - 1]
        tree = Tree()
        tree.addNode(node, None)
        tree = createTree(tree, depth, node)
        gui.drawBoard(node.board)
        #time.sleep(0.5)
    print("Escaped the while loop!")
    #win.getMouse()
    #win.close()
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

solver(board)