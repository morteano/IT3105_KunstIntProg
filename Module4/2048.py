from random import randint, random, choice
import time
from GUI import *

class Node:
    def __init__(self, board, lastMove):
        self.board = board
        self.lastMove = lastMove
        self.children = []


boardSize = 4
inf = float("inf")


# Prints board as text
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


# Moves all tiles to the input direction
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


# Playable game with WASD-buttons as input
def game(board):
    board, dummy, dummy, dummy = spawn(board)
    gui = getNewBoardWindow(4, None)
    while True:
        direction = raw_input("Press direction (WASD): ")
        board, modified = move(board, direction)
        if modified:
            board, dummy, dummy, dummy = spawn(board)
            gui.drawBoard(board)


# Checks if there is possible to perform a legal move
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


# Creates all possible board depending on where the new tile appears
def createAllPossibleBoards(node):
    emptyNodes = []
    for i in range(len(node.board)):
        if node.board[i] == 0:
            emptyNodes.append(i)
    nodeList = []
    for i in emptyNodes:
        child1 = Node(list(node.board), node.lastMove)
        child1.board[i] = 2
        nodeList.append(child1)
    return nodeList


# Uses minimax to get most promising direction to move
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
    return dir, bestIndex


# Unused function to find expectimax heuristics
def findHeuristic(depth, root, heur):
    if depth == 0:
        return heur + heuristicBoard(root.board)
    elif depth % 2 == 1:
        for i in root.children:
            heur += (findHeuristic(depth-1, i, 0))/len(root.children)
        return heur
    else:
        for i in root.children:
            heur += findHeuristic(depth-1, i, 0)/len(root.children)
        return heur


# Search through the tree with alphabeta pruning. But gives the leaf nodes the heuristic of all nodes in the path.
def findHeuristicMiniMaxAlphaBeta(depth, root, heur, alpha, beta):
    heur += heuristicBoard(root.board)
    if depth == 0:
        return heur
    elif depth % 2 == 1:
        v = inf
        for i in root.children:
            v = min(v, findHeuristicMiniMaxAlphaBeta(depth-1, i, heur, alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v
    else:
        v = 0
        for i in root.children:
            v = max(v, findHeuristicMiniMaxAlphaBeta(depth-1, i, heur, alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v


# Returns a heuristic for the board based on a zigzag pattern from the corners
def heuristicBoard(board):
    heuristicList = [200, 100, 50, 25, 20, 18, 16, 12, 10, 8, 7, 6, 5, 4, 3, 2]
    heur = 0
    if max(board) == board[15]:
        heur += board[15]*heuristicList[0]
        heur += board[14]*heuristicList[1]
        heur += board[13]*heuristicList[2]
        heur += board[12]*heuristicList[3]
        heur += board[8]*heuristicList[4]
        heur += board[9]*heuristicList[5]
        heur += board[10]*heuristicList[6]
        heur += board[11]*heuristicList[7]
        heur += board[7]*heuristicList[8]
        heur += board[6]*heuristicList[9]
        heur += board[5]*heuristicList[10]
        heur += board[4]*heuristicList[11]
        heur += board[0]*heuristicList[12]
        heur += board[1]*heuristicList[13]
        heur += board[2]*heuristicList[14]
        heur += board[3]*heuristicList[15]

    elif max(board) == board[0]:
        heur += board[0]*heuristicList[0]
        heur += board[1]*heuristicList[1]
        heur += board[2]*heuristicList[2]
        heur += board[3]*heuristicList[3]
        heur += board[7]*heuristicList[4]
        heur += board[6]*heuristicList[5]
        heur += board[5]*heuristicList[6]
        heur += board[4]*heuristicList[7]
        heur += board[8]*heuristicList[8]
        heur += board[9]*heuristicList[9]
        heur += board[10]*heuristicList[10]
        heur += board[11]*heuristicList[11]
        heur += board[15]*heuristicList[12]
        heur += board[14]*heuristicList[13]
        heur += board[13]*heuristicList[14]
        heur += board[12]*heuristicList[15]

    elif max(board) == board[3]:
        heur += board[3]*heuristicList[0]
        heur += board[2]*heuristicList[1]
        heur += board[1]*heuristicList[2]
        heur += board[0]*heuristicList[3]
        heur += board[4]*heuristicList[4]
        heur += board[5]*heuristicList[5]
        heur += board[6]*heuristicList[6]
        heur += board[7]*heuristicList[7]
        heur += board[11]*heuristicList[8]
        heur += board[10]*heuristicList[9]
        heur += board[9]*heuristicList[10]
        heur += board[8]*heuristicList[11]
        heur += board[12]*heuristicList[12]
        heur += board[13]*heuristicList[13]
        heur += board[14]*heuristicList[14]
        heur += board[15]*heuristicList[15]

    elif max(board) == board[12]:
        heur += board[12]*heuristicList[0]
        heur += board[13]*heuristicList[1]
        heur += board[14]*heuristicList[2]
        heur += board[15]*heuristicList[3]
        heur += board[11]*heuristicList[4]
        heur += board[10]*heuristicList[5]
        heur += board[9]*heuristicList[6]
        heur += board[8]*heuristicList[7]
        heur += board[4]*heuristicList[8]
        heur += board[5]*heuristicList[9]
        heur += board[6]*heuristicList[10]
        heur += board[7]*heuristicList[11]
        heur += board[3]*heuristicList[12]
        heur += board[2]*heuristicList[13]
        heur += board[1]*heuristicList[14]
        heur += board[0]*heuristicList[15]

    # Add a small value for merging tiles
    heur += 10*board.count(0)
    return heur


# Add parent-child relations to the nodes in the tree
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


# Remove parent-child relations to free up memory space
def removeRelations(root):
    for i in root.children:
        for j in i.children:
            j.children = []
        i.children = []
    root = None


# So far unused function for reusing a subtree to make the algorithm faster
def reuseRelations(depth, extraDepth, root):
    if depth == 0:
        addRelations(extraDepth, root)
    else:
        for child in root.children:
            for grandchild in child.children:
                reuseRelations(depth-2, extraDepth, grandchild)


# Tries to solve the game
def solver(board, gui):
    board, random, value, boardIndex = spawn(board)
    depth = 6
    node = Node(board, None)
    addRelations(depth, node)

    while True:
        empty = board.count(0)
        if empty == 0:
            if not legalMoves(board):
                break
        oldNode = node
        gui.drawBoard(node.board)
        dir, index = minimax(depth, node)
        board, modified = move(board, dir)
        board, childIndex, value, boardIndex = spawn(board)
        node = oldNode.children[index].children[childIndex]
        node.board[boardIndex] = value
        node.parent = None
        removeRelations(oldNode)
        addRelations(depth, node)
    gui.drawBoard(node.board)
    return node.board


# Runs the solver iteration number of times and prints the output
def testRuns(iterations):
    gui = getNewBoardWindow(4, None)
    maxTiles = {32:0, 64:0, 128:0, 256:0, 512:0, 1024:0, 2048:0, 4096:0, 8192:0}
    totalTime = 0
    for i in range(iterations):
        board = [0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0]
        start = time.time()
        board = solver(board, gui)
        t = time.time()-start
        print(str(int(t)/60) + " min and " + str(int(t)%60) + " sec")
        print(board)
        maxTiles[max(board)] += 1
        if (i+1) % 10 == 0:
            print(maxTiles)
            print(maxTiles[2048], maxTiles[4096], sum(maxTiles.values()))
            print("Success rate: " + str((float(maxTiles[2048]+maxTiles[4096]))/sum(maxTiles.values())))
        totalTime += t
        time.sleep(3)
    print(maxTiles)
    print("Success rate: " + str(float(maxTiles[2048]+maxTiles[4096]+maxTiles[8192])/sum(maxTiles.values())))
    avgT = totalTime/iterations
    print("Average time was : " + str(int(avgT)/60) + " min and " + str(int(avgT)%60) + " sec")


testRuns(1)