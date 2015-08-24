__author__ = 'MortenAlver'


def getinput(data):
    f = open(data, 'r')
    firstline = f.readline()
    height = firstline[1]
    width = firstline[3]
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
    main()
