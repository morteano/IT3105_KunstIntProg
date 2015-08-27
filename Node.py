__author__ = 'Butikk'



class Node:
    def __init__(self, yPos, xPos):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = 1000 #current distance to the node
        self.heuristic = 1000 #estimated distance to the goal
        self.type = '0' #type of node: '#' for obstacle, '0' for floor, 'S' for start and 'G' for goal
        self.value = 0 #distance + heuristic



