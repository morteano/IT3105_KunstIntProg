__author__ = 'Butikk'



from Node import Node

class Map:

    def __init__(self):

        self.map = []

        self.width = 0
        self.height = 0

    #creates 2D array of map from text file input
    def readMap(self, textFile):
        file = open(textFile)

        firstLine = file.readline()
        firstLine = firstLine.split()

        self.height = int(firstLine[0])
        self.width = int(firstLine[1])

        #create an empty map with corresponding size
        for i in range(self.height):
            self.map.append([])
            for j in range(self.width):
                self.map[i].append(Node(i, j))


        secondLine = file.readline()
        secondLine = secondLine.split()

        #add start and goal position to map
        startNode = self.getPos(int(secondLine[0]), int(secondLine[1]))
        goalNode = self.getPos(int(secondLine[2]), int(secondLine[3]))

        startNode.type = 'S'
        goalNode.type = 'G'



        #add obstacles to map
        for line in file:
            line = line.split()
            for i in range(int(line[2])):
                for j in range(int(line[3])):
                    self.getPos(int(line[0]) + i, int(line[1]) + j).type = '#'

        file.close()

        return startNode, goalNode

    def getPos(self, y, x):
        return self.map[y][x]

    #return array of all adjacent nodes to the current node on the map
    def getNeighbours(self, node):
        #check corners
        if node.yPos == 0 and node.xPos == 0:
            return [self.getPos(node.yPos + 1, node.xPos), self.getPos(node.yPos, node.xPos + 1)]

        elif node.yPos == self.height - 1 and node.xPos == 0:
            return [self.getPos(node.yPos - 1, node.xPos), self.getPos(node.yPos, node.xPos + 1)]

        elif node.yPos == 0 and node.xPos == self.width - 1:
            return [self.getPos(node.yPos + 1, node.xPos), self.getPos(node.yPos, node.xPos - 1)]

        elif node.yPos == self.height - 1 and node.xPos == self.width - 1:
            return [self.getPos(node.yPos, node.xPos - 1), self.getPos(node.yPos - 1, node.xPos)]

        #check edges
        elif node.yPos == 0:
            return [self.getPos(node.yPos + 1, node.xPos), self.getPos(node.yPos, node.xPos - 1), self.getPos(node.yPos, node.xPos + 1)]

        elif node.yPos == self.height - 1:
            return [self.getPos(node.yPos - 1, node.xPos), self.getPos(node.yPos, node.xPos + 1), self.getPos(node.yPos, node.xPos - 1)]

        elif node.xPos == 0:
            return [self.getPos(node.yPos + 1, node.xPos), self.getPos(node.yPos - 1, node.xPos), self.getPos(node.yPos, node.xPos + 1)]

        elif node.xPos == self.width - 1:
            return [self.getPos(node.yPos + 1, node.xPos), self.getPos(node.yPos, node.xPos - 1), self.getPos(node.yPos - 1, node.xPos)]

        #the rest
        else:
            return [self.getPos(node.yPos + 1, node.xPos), self.getPos(node.yPos, node.xPos - 1), self.getPos(node.yPos - 1, node.xPos), self.getPos(node.yPos, node.xPos + 1)]
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
