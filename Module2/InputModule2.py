class Node:
    def __init__(self, nr, xPos, yPos):
        self.id = nr
        self.xPos = xPos
        self.yPos = yPos


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}


def create_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    #board = map(lambda x: x.strip(" "), open(filename, 'r'))

    file = open(filename)
    firstLine = file.readline().split(" ")
    NV = int(firstLine[0]) # Number of vertices
    NE = int(firstLine[1]) # Number of edges

    for i in range(NV):
        line = file.readline().split(" ")
        node = Node(line[0], line[1], line[2])
        csp.variables.append(node)

    for j in range(NE-1):
        line = file.readline().split(" ")


    return 0

create_csp("graph1")