from tkinter import *
from random import randint

class blocks:
    def __init__(self, xx, yy, udt) -> None:
        self.xx = xx
        self.yy = yy
        self.udt = udt
        self.block_place = [[0] * self.yy for _ in range(self.xx)]
        self.current_block = []
        self.standard_blocks = [[[[0, 0], [0, 1], [1, 1], [1, 2]], [[0, 0], [1, 0], [1, 1], [2, 1]]], [[[0, 0], [0, 1], [1, 0], [1, 1]]], [[[0, 0], [0, 1], [0, 2], [0, 3]], [[0, 0], [1, 0], [2, 0], [3, 0]]]]

        self.guiinit()
        pass


    def guiinit(self):
        self.root = Tk()
        self.root.title("BlocksGame@LZH")
        self.root.bind("<Key>", self.key_pressed)
        self.canvas = Canvas(self.root, height=self.xx*20, width=self.yy*20, bg="white")
        self.canvas.grid(row=0, column=0)
        pass

    def ran(self):
        return [randint(0, )]
    
    def start(self):
        pass

    def keypressed(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
        pass


if __name__ == '__main__':
    xx, yy, udt = 20, 10, 100
    game = blocks(xx, yy, udt)
    game.root.mainloop()