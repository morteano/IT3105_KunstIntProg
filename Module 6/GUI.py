from tkinter import *


class GUI(Frame):
    cellColors = {0: "#CCC0B3", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e", 4096: "#3c3a32"}

    def __init__(self, parent, size):
        Frame.__init__(self, parent, bg="#BBADA0")

        self.parent = parent
        self.cells = []
        self.initUI(size, 150)
        self.pack()


    def initUI(self, boardSize, cellSize):
        for row in range(boardSize-1, -1, -1):
            self.cells.append([])
            for column in range(boardSize):
                cell = Frame(self, width=cellSize, height=cellSize)
                cell.grid(row=row, column=column, padx=4, pady=4)
                cell.pack_propagate(0)

                tile = Label(cell, bg="#CCC0B3", font=("Helvetica", 35, "bold"))
                tile.pack(fill=BOTH, expand=1)
                self.cells[-1].append(tile)


    def setTile(self, value, x, y):
        self.cells[y][x].config({"bg": GUI.cellColors[min(4096, value)], "fg": ("#776E65" if value < 8 else "#f9f6f2"), "text": str(value) if value else ''})


    def drawBoard(self, board):
        for col in range(4):
            for row in range(4):
                self.setTile(board[col*4+row], col, row)


def getNewBoardWindow(size=4, listener=None):
    root = Tk()
    root.title("2048")
    if listener: root.bind("<Key>", listener)

    return GUI(root, size)


#mainThread = Thread(target=self.AI)
#mainThread.start()
#self.gui.mainloop()