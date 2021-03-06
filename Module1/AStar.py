# Data structure for the HeapQueue class
import heapq
import math
from Map import Map
from graphics import *
import time

# Priority queue with heap as data structure
class HeapQueue:
    def __init__(self):
        self.elements = []

    # Checks if heap is empty
    def empty(self):
        return len(self.elements) == 0

    # Adds element to the heap and makes sure the node with lowest value is on top
    def insert(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    #returns the element with lowest value and removes it from the heap
    def get(self):
        return heapq.heappop(self.elements)[1]

class Stack:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def insert(self, item, dummyValue):
        self.elements.append(item)

    def get(self):
        return self.elements.pop()


#display graphical map
def displayMap(map, (path, examined)):
    #create graphics window with size 500x500
    win = GraphWin("A Star", 500, 500)

    #create rectangles corresponding to the map, where black is wall, red is start point and green is goal point
    for i in range(map.height):
        for j in range(map.width):
            rectangle = Rectangle(Point((20 * j) + 10, (20 * i) + 10), Point((20 * j) + 30, (20 * i) + 30))
            if map.getPos(i, j).type == '#':
                rectangle.setFill("black")
            elif map.getPos(i, j).type == 'S':
                rectangle.setFill("red")
            elif map.getPos(i, j).type == 'G':
                rectangle.setFill("green")

            #draw rectangle to the graphics window
            rectangle.draw(win)

    #draw the resulting path from the A Star algorithm as black circles
    for i in path:
        circle = Circle(Point(20 * i.xPos + 20, 20 * i.yPos + 20), 5)
        circle.setFill("black")

        circle.draw(win)

    #draw the examined nodes as crosses
    for i in examined:
        if i not in path:
            line1 = Line(Point(20 * i.xPos + 15, 20 * i.yPos + 15), Point(20 * i.xPos + 26, 20 * i.yPos + 26))
            line2 = Line(Point(20 * i.xPos + 15, 20 * i.yPos + 25), Point(20 * i.xPos + 26, 20 * i.yPos + 14))

            line1.setFill("black")
            line2.setFill("black")

            line1.draw(win)
            line2.draw(win)

    #makes sure the window does not close immediately. Close the window by clicking on it
    win.getMouse()

#manhattan distance
def heuristic(nodeY, nodeX, goalY, goalX, type):
    if type == "Astar":
        return math.fabs(goalX - nodeX) + math.fabs(goalY - nodeY)
    return 0

#the main algorithm
def searchAlgorithm(map, startY, startX, goalY, goalX, type, win):
    startNode = map.getPos(startY, startX)
    startNode.distance = 0
    startNode.heuristic = heuristic(startY, startX, goalY, goalX, type)
    startNode.value = startNode.distance + startNode.heuristic

    #all nodes that have been examined
    examined = []

    #dictionary to keep track of previous nodes, so the path can be created in the end
    cameFrom = {}
    cameFrom[startNode] = None
    if type == "DFS":
        priorityQueue = Stack()
    else:
        priorityQueue = HeapQueue()
    priorityQueue.insert(startNode, startNode.value)

    currentNode = startNode
    nrOfNodes = 0

    solved = False

    graphicRects = {}

    #create rectangles corresponding to the map, where black is wall, red is start point and green is goal point
    for i in range(map.height):
        for j in range(map.width):
            rectangle = Rectangle(Point((20 * j) + 10, (20 * i) + 10), Point((20 * j) + 30, (20 * i) + 30))
            if map.getPos(i, j).type == '#':
                rectangle.setFill("black")
                graphicRects[map.getPos(i, j)] = [rectangle, "black"]
            elif map.getPos(i, j).type == 'S':
                rectangle.setFill("red")
                graphicRects[map.getPos(i, j)] = [rectangle, "red"]
            elif map.getPos(i, j).type == 'G':
                rectangle.setFill("green")
                graphicRects[map.getPos(i, j)] = [rectangle, "green"]
            else:
                rectangle.setFill("white")
                graphicRects[map.getPos(i, j)] = [rectangle, "white"]

            #draw rectangle to the graphics window
            rectangle.draw(win)


    while not priorityQueue.empty():

        finalPath = [currentNode]
        while currentNode != startNode:
            currentNode = cameFrom[currentNode]
            finalPath.append(currentNode)
        for i in finalPath:
            if graphicRects[i][1] == "white":
                graphicRects[i][0].setFill("blue")
                graphicRects[i][1] = "blue"
        for i in range(map.height):
            for j in range(map.width):
                if graphicRects[map.getPos(i, j)][1] == "blue":
                    if map.getPos(i, j) not in finalPath:
                        graphicRects[map.getPos(i, j)][0].setFill("white")
                        graphicRects[map.getPos(i, j)][1] = "white"



        #choose the most promising node
        currentNode = priorityQueue.get()

        #make sure it is not examined again
        examined.append(currentNode)


        #if the goal is reached, break out of the loop
        if map.getPos(goalY, goalX) == currentNode:
            solved = True
            break

        #find all neighbours of the current node
        neighbours = map.getNeighbours(currentNode)


        #go through all neighbours which are not obstacles and not examined before
        for i in neighbours:
            if i.type != '#' and i not in examined:

                #if the the distance to i from the current node is smaller than the previous distance,
                #then calculate its new value and add it to the priority queue, and update its 'cameFrom' node
                if i.distance > currentNode.distance + 1:
                    i.distance = currentNode.distance + 1
                    i.heuristic = heuristic(i.yPos, i.xPos, goalY, goalX, type)
                    i.value = i.distance + i.heuristic

                    priorityQueue.insert(i, i.value)

                    cameFrom[i] = currentNode
        nrOfNodes += 1

    print("Number of nodes: " + str(nrOfNodes))
    # Create path from goal to start

    wasSolved(solved)

    finalPath = [currentNode]
    while currentNode != startNode:
        currentNode = cameFrom[currentNode]
        finalPath.append(currentNode)
    for i in finalPath:
        if graphicRects[i][1] == "white":
            graphicRects[i][0].setFill("blue")
            graphicRects[i][1] = "blue"
    for i in range(map.height):
        for j in range(map.width):
            if graphicRects[map.getPos(i, j)][1] == "blue":
                if map.getPos(i, j) not in finalPath:
                    graphicRects[map.getPos(i, j)][0].setFill("white")
                    graphicRects[map.getPos(i, j)][1] = "white"



    return finalPath, examined

def wasSolved(solved):
    if not solved:
        print("Map is not solvable")

map = Map()

mapInput = raw_input("Enter map text file: ")


start, goal = map.readMap(mapInput)


win1 = GraphWin("A Star", 500, 500)
(nrOfNodes, pathLen) = searchAlgorithm(map, start.yPos, start.xPos, goal.yPos, goal.xPos, "Astar", win1)
print("Number of nodes for A*: " + str(nrOfNodes))
print("Number of nodes in path for A*: " + str(pathLen))

map2 = Map()
start, goal = map2.readMap(mapInput)
win2 = GraphWin("BFS", 500, 500)
(nrOfNodes, pathLen) = searchAlgorithm(map2, start.yPos, start.xPos, goal.yPos, goal.xPos, "BFS", win2)
print("Number of nodes for BFS: " + str(nrOfNodes))
print("Number of nodes in path for BFS: " + str(pathLen))

map3 = Map()
start, goal = map3.readMap(mapInput)
win3 = GraphWin("DFS", 500, 500)
(nrOfNodes, pathLen) = searchAlgorithm(map3, start.yPos, start.xPos, goal.yPos, goal.xPos, "DFS", win3)
print("Number of nodes for DFS: " + str(nrOfNodes))
print("Number of nodes in path for DFS: " + str(pathLen))

win3.getMouse()
win3.close()


#displayMap(map, result)