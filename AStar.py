# Data structure for the HeapQueue class
import heapq
import math
from Map import Map
from graphics import *

solved = False


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

#display graphical map
def displayMap(map, path):
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

    #draw the resulting path from the A Star algorithm
    for i in path:
        circle = Circle(Point(20 * i.xPos + 20, 20 * i.yPos + 20), 5)
        circle.setFill("black")

        circle.draw(win)

    #makes sure the window does not close immediately. Close the window by clicking on it
    win.getMouse()

#manhattan distance
def heuristic(nodeY, nodeX, goalY, goalX):
    return math.fabs(goalX - nodeX) + math.fabs(goalY - nodeY)

#the main algorithm
def aStar(map, startY, startX, goalY, goalX):
    startNode = map.getPos(startY, startX)
    startNode.distance = 0
    startNode.heuristic = heuristic(startY, startX, goalY, goalX)
    startNode.value = startNode.distance + startNode.heuristic

    #all nodes that have been examined
    examined = []

    #dictionary to keep track of previous nodes, so the path can be created in the end
    cameFrom = {}
    cameFrom[startNode] = None

    priorityQueue = HeapQueue()
    priorityQueue.insert(startNode, startNode.value)

    currentNode = startNode
    nrOfNodes = 0

    while not priorityQueue.empty():

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
                    i.heuristic = heuristic(i.yPos, i.xPos, goalY, goalX)
                    i.value = i.distance + i.heuristic

                    priorityQueue.insert(i, i.value)

                    cameFrom[i] = currentNode
        nrOfNodes += 1
    print("Number of nodes: " + str(nrOfNodes))
    #create path from goal to start

    finalPath = [currentNode]
    while currentNode != startNode:
        currentNode = cameFrom[currentNode]
        finalPath.append(currentNode)
    return finalPath



map = Map()
start, goal = map.readMap("input6.txt")

#displays the map with the resulting path with graphics
result = aStar(map, start.yPos, start.xPos, goal.yPos, goal.xPos)
if solved:
    displayMap(map, result)
else:
    print("Map is not solvable")
    displayMap(map, result)
