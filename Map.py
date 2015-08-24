__author__ = 'Butikk'

#COMPLETE

from Node import Node

class Map:

    def __init__(self):

        self.map = []

        self.width = 0
        self.height = 0

    def readMap(self, textFile):
        file = open(textFile)

        firstLine = file.readline()
        firstLine = firstLine.split()

        self.width = int(firstLine[0])
        self.height = int(firstLine[1])

        #create an empty map with corresponding size
        for i in range(self.height):
            self.map.append([])
            for j in range(self.width):
                self.map[i].append(Node(j, i))

        secondLine = file.readline()
        secondLine = secondLine.split()

        #add start and goal position to map
        self.map[int(secondLine[1])][int(secondLine[0])].type = 'S'
        self.map[int(secondLine[3])][int(secondLine[2])].type = 'G'

        #add obstacles to map
        for line in file:
            line = line.split()
            for i in range(int(line[3])):
                for j in range(int(line[2])):
                    self.map[int(line[1]) + i][int(line[0]) + j].type = '#'


        file.close()

    def getPos(self, x, y):
        return self.map[y][x]
"""
    def printMap(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.getPos(i, j).type)"""

"""
def getinput(data):
    f = open(data, 'r')
    firstline = f.readline()
    height = firstline.split(",")[0][1:]
    width = firstline.split(",")[1][0:-2]
    secondline = f.readline()
    start = (secondline[1], secondline[3])
    goal = (secondline[6], secondline[8])

    for line in f:
            print(line)

    return height, width, start, goal


def main():
    height, width, start, goal = getinput("input0.txt")
    print("Height: " + height)
    print("Width: " + width)
    print("Start: (" + start[0] + ", " + start[1] + ")")
    print("Goal: (" + goal[0] + ", " + goal[1] + ")")

if __name__ == "__main__":
    main()"""
