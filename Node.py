__author__ = 'Butikk'

#COMPLETE

class Node:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = 1000
        self.heuristic = 1000
        self.type = '0'
        self.value = 0

    def updateValue(self):
        self.value = self.distance + self.heuristic

