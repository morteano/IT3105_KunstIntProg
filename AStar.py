__author__ = 'MortenAlver'

import math
from Map import Map
from HeapQueue import HeapQueue
from graphics import *

map = Map()
map.readMap("input1.txt")

#display graphical map
def displayMap(map):
    #create graphics window with size 500x500
    win = GraphWin("A Star", 500, 500)

    #create rectangles corresponding to the map, where black is wall, red is start point and green is goal point
    for i in range(map.height):
        for j in range(map.width):
            rectangle = Rectangle(Point((20 * i) + 10, (20 * j) + 10), Point((20 * i) + 30, (20 * j) + 30))
            if map.getPos(i, j).type == '#':
                rectangle.setFill("black")
            elif map.getPos(i, j).type == 'S':
                rectangle.setFill("red")
            elif map.getPos(i, j).type == 'G':
                rectangle.setFill("green")

            #draw rectangle to the graphics window
            rectangle.draw(win)

    #makes sure the window does not close immediately. Close the window by clicking on it
    win.getMouse()

#manhattan distance
def heuristic(nodeX, nodeY, goalX, goalY):
    return math.abs((goalX - nodeX) + (goalY - nodeY))

#the main algorithm
def aStar(map, startX, startY, goalX, goalY):
    startNode = map.getPos(startX, startY)
    startNode.distance = 0
    startNode.heuristic = heuristic(startX, startY, goalX, goalY)
    startNode.updateValue()

    priorityQueue = HeapQueue()
    priorityQueue.insert(startNode)

    #TODO


