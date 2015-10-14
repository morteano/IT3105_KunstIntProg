from random import randint, random, choice
from graphics import *
import heapq
import time
from copy import deepcopy
from visuals import GameWindow
from Tree import *
from GUI import *


class Node:
    def __init__(self, board, lastMove):
        self.board = board
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
    modified = False
    if direction == 'a':
        board,  modified = moveLeft(board)
    elif direction == "d":
        board,  modified = moveRight(board)
    elif direction == "w":
        board,  modified = moveUp(board)
    elif direction == "s":
        board,  modified = moveDown(board)
    return board, modified


def moveLeft(board):
    modified = False
    for i in range(boardSize):
        tempValue = 0
        index = 0
        for j in range(boardSize):
            if tempValue != 0:
                if tempValue == board[boardSize*i+j]:
                    modified = True
                    board[tempNodeIndex] *= 2
                    board[boardSize*i+j] = 0
                    tempValue = 0
            if board[boardSize*i+j] != 0:
                tempValue = board[boardSize*i+j]
                if j != index:
                    modified = True
                    board[boardSize*i+index] = board[boardSize*i+j]
                    board[boardSize*i+j] = 0
                tempNodeIndex = boardSize*i+index
                index += 1
    return board, modified


def moveRight(board):
    modified = False
    for i in range(boardSize):
        tempValue = 0
        index = boardSize - 1
        for j in range(boardSize - 1, -1, -1):
            if tempValue != 0:
                if tempValue == board[boardSize*i+j]:
                    modified = True
                    board[tempNodeIndex] *= 2
                    board[boardSize*i+j] = 0
                    tempValue = 0
            if board[boardSize*i+j] != 0:
                tempValue = board[boardSize*i+j]
                if j != index:
                    modified = True
                    board[boardSize*i+index] = board[boardSize*i+j]
                    board[boardSize*i+j] = 0
                tempNodeIndex = boardSize*i+index
                index -= 1
    return board, modified


def moveUp(board):
    modified = False
    for i in range(boardSize):
        tempValue = 0
        index = 0
        for j in range(boardSize):
            if tempValue != 0:
                if tempValue == board[boardSize*j+i]:
                    modified = True
                    board[tempNodeIndex] *= 2
                    board[boardSize*j+i] = 0
                    tempValue = 0
            if board[boardSize*j+i] != 0:
                tempValue = board[boardSize*j+i]
                if j != index:
                    modified = True
                    board[boardSize*index+i] = board[boardSize*j+i]
                    board[boardSize*j+i] = 0
                tempNodeIndex = boardSize*index+i
                index += 1
    return board, modified


def moveDown(board):
    modified = False
    for i in range(boardSize):
        tempValue = 0
        index = boardSize - 1
        for j in range(boardSize - 1, -1, -1):
            if tempValue != 0:
                if tempValue == board[boardSize*j+i]:
                    modified = True
                    board[tempNodeIndex] *= 2
                    board[boardSize*j+i] = 0
                    tempValue = 0
            if board[boardSize*j+i] != 0:
                tempValue = board[boardSize*j+i]
                if j != index:
                    modified = True
                    board[boardSize*index+i] = board[boardSize*j+i]
                    board[boardSize*j+i] = 0
                tempNodeIndex = boardSize*index+i
                index -= 1
    return board, modified


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


def createAllPossibleBoards(node):
    emptyNodes = []
    for i in range(len(node.board)):
        if node.board[i] == 0:
            emptyNodes.append(i)
    nodeList = []
    for i in emptyNodes:
        child1 = Node(list(node.board), node.lastMove)
        child1.board[i] = 2
        child2 = Node(list(node.board), node.lastMove)
        child2.board[i] = 4
        nodeList.append(child1)
        nodeList.append(child2)
    return nodeList


def minimax(depth, root):
    maxHeuristic = -1
    dir = ""
    bestIndex = 0
    index = 0
    for i in root.children:
        heurI = findHeuristic(depth-1, i, 0)
        if  heurI > maxHeuristic:
            maxHeuristic = heurI
            dir = i.lastMove
            bestIndex = index
        index += 1
    return dir, bestIndex

def findHeuristic(depth, root, heur):
    if depth == 0:
        return heur + heuristic5(root.board)
    elif depth % 2 == 1:
        it = 0
        for i in root.children:
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

def heuristic2(board):
    empty = 0
    index = board.index(max(board))
    if index == 0 or max(board) == 3 or max(board) == 12 or max(board) == 15:
        empty = 10000
        tempBoard = list(board)
        tempBoard[index] = 0
        nextIndex = board.index(max(tempBoard))
        temp2Board = list(board)
        temp2Board[nextIndex] = 0
        next2Index = board.index(max(tempBoard))
        if nextIndex == 1 and next2Index == 4 or next2Index == 1 and nextIndex == 4:
            empty -= 100
        elif nextIndex == 1 or nextIndex == 4:
            empty += 500
        if next2Index == 5:
            empty += 400

    for i in range(len(board)):
        if board[i] == 0:
            empty += 500
    return empty

def heuristic3(board):
    heur = 10*board[0]+5*board[1]+5*board[4]+3*board[5]
    for i in range(len(board)):
        if board[i] == 0:
            heur += 5
    return heur


def heuristic4(board):
    heur = 20*board[12]+15*board[13]+8*board[8]+12*board[9]+7*board[4]+10*board[14]
    for i in range(len(board)):
        if board[i] == 0:
            heur += 5
    return heur


def heuristic5(board):
    heur = 0
    for i in range(len(board)):
        if i in [0, 1, 2, 3, 12, 13, 14, 15]:
            heur += board[i]
        if i in [0, 4, 8, 12, 3, 7, 11, 15]:
            heur += board[i]
        if i in [0, 12, 3, 15]:
            heur += board[i]
    for j in range(len(board)):
        if board[i] == 0:
            heur += 100
    return heur


def heuristic6(board):
    heur = 0
    for i in range(len(board)):
        if i in [0, 1, 2, 3, 12, 13, 14, 15]:
            heur += board[i]*board[i]
        if i in [0, 4, 8, 12, 3, 7, 11, 15]:
            heur += board[i]*board[i]
        if i in [0, 12, 3, 15]:
            heur += board[i]*board[i]
    for j in range(len(board)):
        if board[i] == 0:
            heur += 1000
    return heur

def addRelations(depth, root):
    if depth == 0:
        return
    for i in ["a", "d", "w", "s"]:
        board = list(root.board)
        board, modified = move(board, i)
        if modified:
            node = Node(board, i)
            node.parent = root
            root.children.append(node)

    for i in root.children:
        children = createAllPossibleBoards(i)

        for j in children:
            j.parent = i
            i.children.append(j)
            addRelations(depth - 2, j)


def removeRelations(root):
    for i in root.children:
        for j in i.children:
            j.children = []
        i.children = []
    root = None


def solver(board, gui):
    board, random, value = spawn(board)
    depth = 4

    node = Node(board, None)
    addRelations(depth, node)

    full = False
    while True:
        empty = 0
        for tile in board:
            if tile == 0:
                empty += 1
        if empty == 0:
            if not legalMoves(board):
                break
        elif empty < 1 and max(board) > 1024:
            depth = 10
        elif empty < 3 and max(board) > 256:
            depth = 8
        elif empty < 6 and max(board) > 128:
            depth = 6
        # elif max(board) > 128:
        #     depth = 4
        else:
            depth = 4

        oldNode = node
        dir, index = minimax(depth, node)
        board, modified = move(board, dir)
        board, childIndex, value = spawn(board)
        node = oldNode.children[index].children[(childIndex * 2) + (value / 2) - 1]
        node.parent = None
        removeRelations(oldNode)
        addRelations(depth, node)
        gui.drawBoard(node.board)
        #time.sleep(0.1)
    print("Escaped the while loop!")
    return node.board
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

gui = getNewBoardWindow(4, None)
for i in range(10):
    board = [0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0]
    start = time.time()
    board = solver(board, gui)
    t = time.time()-start
    print(str(int(t)/60) + " min and " + str(int(t)%60) + " sec")
    print board