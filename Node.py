__author__ = 'Butikk'

class Node:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = 1000
        self.heuristic = 1000
        self.value = self.distance + self.heuristic
