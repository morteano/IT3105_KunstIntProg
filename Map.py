__author__ = 'Butikk'

class Map:

	def __init__(self):

		self.map = []

		self.width = 0
		self.height = 0

		self.readMap("Map.txt")

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
				self.map[i].append('0')

		secondLine = file.readline()
		secondLine = secondLine.split()

		#add start and goal position to map
		self.map[int(secondLine[1])][int(secondLine[0])] = 's'
		self.map[int(secondLine[3])][int(secondLine[2])] = 'g'

		#add obstacles to map
		for line in file:
			line = line.split()
			for i in range(int(line[3])):
				for j in range(int(line[2])):
					self.map[int(line[1]) + i][int(line[0]) + j] = '1'


		file.close()

	def getPos(self, x, y):
		return self.map[y][x]

	def printMap(self):
		for i in range(self.height - 1, -1, -1):
			print(self.map[i])
