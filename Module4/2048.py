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
inf = float("inf")


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
    return board, random, board[emptyNodes[random]], emptyNodes[random]


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
        # child2 = Node(list(node.board), node.lastMove)
        # child2.board[i] = 4
        nodeList.append(child1)
        # nodeList.append(child2)
    return nodeList


def minimax(depth, root):
    maxHeuristic = -1
    dir = ""
    bestIndex = 0
    index = 0
    for i in root.children:
        heurI = findHeuristicMiniMaxAlphaBeta(depth-1, i, 0, -inf, inf)
        if  heurI > maxHeuristic:
            maxHeuristic = heurI
            dir = i.lastMove
            bestIndex = index
        index += 1
    # if heurI < 1:
    #     print("Heuristic: ", heurI)
    return dir, bestIndex

def findHeuristic(depth, root, heur):
    if depth == 0:
        return heur + heuristicMiniMe(root.board)
    elif depth % 2 == 1:
        for i in root.children:
            heur += (findHeuristic(depth-1, i, 0))/len(root.children)
        return heur
    else:
        for i in root.children:
            heur += findHeuristic(depth-1, i, 0)/len(root.children)
        return heur


def findHeuristicMiniMax(depth, root, heur):
    heurMax = 0
    heurMin = 100000000
    if depth == 0:
        return heur + heuristicMagne(root.board)
    elif depth % 2 == 1:
        for i in root.children:
            tempHeur = findHeuristicMiniMax(depth-1, i, 0)
            if tempHeur < heurMin:
                heurMin = tempHeur
        return heurMin
    else:
        # if len(root.children) == 0:
            # print("Len: ", len(root.children))
        for i in root.children:
            tempHeur = findHeuristicMiniMax(depth-1, i, 0)
            if tempHeur > heurMax:
                heurMax = tempHeur
        return heurMax

def findHeuristicMiniMaxAlphaBeta(depth, root, heur, alpha, beta):
    if depth == 0:
        return heur + heuristicMagne(root.board)
    elif depth % 2 == 1:
        v = inf
        for i in root.children:
            v = min(v, findHeuristicMiniMaxAlphaBeta(depth-1, i, 0, alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v
    else:
        v = -inf
        for i in root.children:
            v = max(v, findHeuristicMiniMaxAlphaBeta(depth-1, i, 0, alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v


def heuristic5(board):
    # {64: 0, 128: 0, 4096: 0, 1024: 17, 256: 2, 512: 11, 2048: 1}
    heur = 0
    for i in range(len(board)):
        if i in [0, 1, 2, 3, 12, 13, 14, 15]:
            heur += board[i]
        if i in [0, 4, 8, 12, 3, 7, 11, 15]:
            heur += board[i]
        if i in [0, 12, 3, 15]:
            heur += board[i]
        heur += 100*board.count(0)
    return heur


def heuristicDownLeft(board):
    maxTile = max(board)
    heur = 0
    if maxTile == board[12]:
        heur += board[12]*10000
        heur += board[13]*20
        heur += board[14]*10
        heur += board[15]*4
        heur += board[8]*3
        heur += board[9]*2
        for i in [0,1,2,3,4,5,6,7,10,11]:
            heur -= board[i]*(i%boardSize)*((boardSize-1)-(i/boardSize))
    elif maxTile == board[0]:
        heur += board[0]*10000
        heur += board[1]*20
        heur += board[2]*10
        heur += board[3]*4
        heur += board[4]*3
        heur += board[5]*2
        for i in [6,7,8,9,10,11,12,13,14,15]:
            heur -= board[i]*(i%boardSize)*(i/boardSize)
    elif maxTile == board[3]:
        heur += board[3]*10000
        heur += board[2]*20
        heur += board[1]*10
        heur += board[0]*4
        heur += board[7]*3
        heur += board[6]*2
        for i in [4,5,8,9,10,11,12,13,14,15]:
            heur -= board[i]*((boardSize-1)-i%boardSize)*(i/boardSize)
    elif maxTile == board[15]:
        heur += board[15]*10000
        heur += board[14]*20
        heur += board[13]*10
        heur += board[12]*4
        heur += board[11]*3
        heur += board[10]*2
        for i in [0,1,2,3,4,5,6,7,8,9]:
            heur -= board[i]*((boardSize-1)-i%boardSize)*((boardSize-1)-i/boardSize)
    else:
        heur = heuristic5(board)/10
        return heur
    if maxTile == 2048:
        heur += 2048*2048
    heur += 50*board.count(0)
    return heur


def heuristicMiniMe(board):
    #depth = 3: {32: 0, 64: 0, 4096: 2, 512: 13, 128: 1, 2048: 44, 256: 0, 1024: 40}
    heur = 0
    heur += board[12]*100
    heur += board[13]*50
    heur += board[14]*20
    heur += board[15]*6
    for i in range(boardSize*2):
        heur -= board[i]

    heur += 10*board.count(0)
    return heur


def heuristicMiniMe2(board):
    heur = 0
    heur += board[12]*100
    heur += board[13]*50
    heur += board[14]*20
    heur += board[15]*6
    heur += board[11]*4
    if max(board) == board[13]:
        if board[12] > board[8]:
            heur += board[8]*50

    for i in range(boardSize*2):
        heur -= board[i]

    heur += 10*board.count(0)
    return heur

def heuristicMiniMeExtended(board):
    # {32: 0, 64: 0, 4096: 10, 512: 12, 128: 0, 2048: 41, 256: 0, 1024: 37}
    heur = 0
    heur += board[12]*100
    heur += board[13]*50
    heur += board[14]*20
    heur += board[15]*10
    heur += board[11]*6
    heur += board[10]*5
    heur += board[9]*4
    heur += board[8]*3
    if max(board) == board[13]:
        if board[12] > board[8]:
            heur += board[8]*50

    for i in range(boardSize*2):
        heur -= board[i]

    heur += 10*board.count(0)
    return heur


def heuristicMiniMeDoubled(board):
    heur = 0
    if max(board) == board[15]:
        heur += board[15]*100
        heur += board[14]*50
        heur += board[13]*20
        heur += board[12]*10
        heur += board[8]*6
        heur += board[9]*5
        heur += board[10]*4
        heur += board[11]*3
        if max(board) == board[14]:
            if board[15] > board[11]:
                heur += board[11]*50
    else:
        heur += board[12]*100
        heur += board[13]*50
        heur += board[14]*20
        heur += board[15]*10
        heur += board[11]*6
        heur += board[10]*5
        heur += board[9]*4
        heur += board[8]*3
        if max(board) == board[13]:
            if board[12] > board[8]:
                heur += board[8]*50


    for i in range(boardSize*2):
        heur -= board[i]
    heur += 10*board.count(0)
    return heur

def heuristicMagne(board):
    # {32: 0, 64: 0, 4096: 17, 512: 5, 128: 1, 2048: 54, 256: 0, 1024: 23}
    heur = 0
    if max(board) == board[15]:
        heur += board[15]*200
        heur += board[14]*100
        heur += board[13]*50
        heur += board[12]*25
        heur += board[8]*20
        heur += board[9]*18
        heur += board[10]*16
        heur += board[11]*12
        heur += board[7]*10
        heur += board[6]*8
        heur += board[5]*7
        heur += board[4]*6
        heur += board[0]*5
        heur += board[1]*4
        heur += board[2]*3
        heur += board[3]*2

        if max(board) == board[14]:
            if board[15] > board[11]:
                heur += board[11]*50
    elif max(board) == board[0]:
        heur += board[0]*200
        heur += board[1]*100
        heur += board[2]*50
        heur += board[3]*25
        heur += board[7]*20
        heur += board[6]*18
        heur += board[5]*16
        heur += board[4]*12
        heur += board[8]*10
        heur += board[9]*8
        heur += board[10]*7
        heur += board[11]*6
        heur += board[15]*5
        heur += board[14]*4
        heur += board[13]*3
        heur += board[12]*2
    elif max(board) == board[3]:
        heur += board[3]*200
        heur += board[2]*100
        heur += board[1]*50
        heur += board[0]*25
        heur += board[4]*20
        heur += board[5]*18
        heur += board[6]*16
        heur += board[7]*12
        heur += board[11]*10
        heur += board[10]*8
        heur += board[9]*7
        heur += board[8]*6
        heur += board[12]*5
        heur += board[13]*4
        heur += board[14]*3
        heur += board[15]*2

    elif max(board) == board[12]:
        heur += board[12]*200
        heur += board[13]*100
        heur += board[14]*50
        heur += board[15]*25
        heur += board[11]*20
        heur += board[10]*18
        heur += board[9]*16
        heur += board[8]*12
        heur += board[4]*10
        heur += board[5]*8
        heur += board[6]*7
        heur += board[7]*6
        heur += board[3]*5
        heur += board[2]*4
        heur += board[1]*3
        heur += board[0]*2
        if max(board) == board[13]:
            if board[12] > board[8]:
                heur += board[8]*50

    heur += 10*board.count(0)
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


def reuseRelations(depth, extraDepth, root):
    if depth == 0:
        addRelations(extraDepth, root)
    else:
        for child in root.children:
            for grandchild in child.children:
                reuseRelations(depth-2, extraDepth, grandchild)


def solver(board, gui):
    board, random, value, boardIndex = spawn(board)
    depth = 4
    #oldDepth = 4
    node = Node(board, None)
    addRelations(depth, node)

    while True:
        empty = board.count(0)
        if empty == 0:
            if not legalMoves(board):
                break
        elif empty < 1 and max(board) > 1024:
            depth = 10
        elif empty < 3 and max(board) > 256:
            depth = 8
        elif empty < 6 and max(board) > 128:
            depth = 6
        elif empty < 2:
            depth = 8
        else:
            depth = 6
        oldNode = node
        dir, index = minimax(depth, node)
        board, modified = move(board, dir)
        board, childIndex, value, boardIndex = spawn(board)
        node = oldNode.children[index].children[childIndex]
        node.board[boardIndex] = value
        node.parent = None
        removeRelations(oldNode)
        #reuseRelations(oldDepth-2, 2+depth-oldDepth, node)
        addRelations(depth, node)
        #oldDepth = depth
        gui.drawBoard(node.board)
        #time.sleep(0.1)
    return node.board
    #win.getMouse()
    #win.close()

gui = getNewBoardWindow(4, None)
maxTiles = {32:0, 64:0, 128:0, 256:0, 512:0, 1024:0, 2048:0, 4096:0}
for i in range(100):
    board = [0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0]
    start = time.time()
    board = solver(board, gui)
    t = time.time()-start
    print(str(int(t)/60) + " min and " + str(int(t)%60) + " sec")
    print board
    maxTiles[max(board)] += 1
    if i % 10 == 0:
        print("Magne")
        print(maxTiles)
    time.sleep(3)
print(maxTiles)