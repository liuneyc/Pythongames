'''
2024.10.22
于习概课
'''

from random import randint
from tkinter import *
from tkinter import messagebox

class Saolei:
    def __init__(self, xx, yy, bomb) -> None:
        """
        初始化
        """
        self.xx = xx
        self.yy = yy
        self.bombnum = bomb

        self.dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        self.dy = [-1, 0, 1, -1, 1, -1, 0, 1]

        self.isstart = 0
        
        self.root = Tk()
        self.root.title("SLGame")

        self.btn = [[None for _ in range(yy)] for _ in range(xx)]
        self.mapp = [[0 for _ in range(yy)] for _ in range(xx)]
        self.marklist = []
        self.guiinit()
        self.setbomb()


    def guiinit(self):
        """
        gui初始化
        """
        for x in range(xx):
            for y in range(yy):
                btntmp = Button(self.root, width = 2, height = 1, bg = "grey", command = lambda x0 = x, y0 = y : self.click(x0, y0))
                btntmp.bind("<Button-3>", lambda event, x0 = x, y0 = y : self.rightclick(x0, y0))
                btntmp.grid(row=x, column=y)
                self.btn[x][y] = btntmp


    def setbomb(self):
        """
        放置雷
        """
        self.bombs = []
        self.mapp = [[0 for _ in range(yy)] for _ in range(xx)]
        while len(self.bombs) < self.bombnum:
            x0 = randint(0, self.xx - 1)
            y0 = randint(0, self.yy - 1)
            if self.mapp[x0][y0] == 0:
                self.mapp[x0][y0] = -1
                self.bombs.append([x0, y0])
        for x in range(xx):
            for y in range(yy):
                if self.mapp[x][y] == -1:
                    for i in range(8):
                        if self.check(x+self.dx[i], y+self.dy[i]) and self.mapp[x+self.dx[i]][y+self.dy[i]] != -1 :
                            self.mapp[x+self.dx[i]][y+self.dy[i]] += 1
    

    def click(self, x, y):
        """
        按button
        """
        if self.isstart == 0:
            self.start(x, y)
        btntmp = self.btn[x][y]
        if self.mapp[x][y] == -1:
            self.isstart = 0
            self.end()
            return
        elif btntmp["text"] != "" and btntmp["bg"] == "white":
            self.autoopen(x, y)
        elif self.mapp[x][y] == 0:
            self.opendfs(x, y)
        elif self.mapp[x][y] > 0:
            btntmp["text"] = self.mapp[x][y]
            btntmp["bg"] = "white"
        
    
    def rightclick(self, x, y):
        """
        雷的标记
        """
        if self.isstart == 0:
            return
        btntmp = self.btn[x][y]
        if btntmp["text"] == "":
            if self.mark >= self.bombnum:
                return
            else:
                btntmp["text"] = "*"
                btntmp["bg"] = "grey"
                self.marklist.append([x, y])
        elif btntmp["text"] == "*":
            btntmp["text"] = ""
            btntmp["bg"] = "grey"
            self.marklist.remove([x, y])
        if len(self.marklist) == self.bombnum:
            self.checkwin()
    

    def start(self, x, y):
        """
        第一次按
        """
        while(self.mapp[x][y] != 0):
            self.setbomb()
        
        self.isstart = 1
        self.mark = 0
        for i in range(self.xx):
            for j in range(self.yy):
                self.btn[i][j]["text"] = ""
                self.btn[i][j]["bg"] = "grey"


    def check(self, x, y) -> bool:
        """
        检测是否越界 1 / 0 
        """
        return 1 if 0 <= x < self.xx and 0 <= y < self.yy else 0
            

    def end(self):
        for i in self.bombs:
            self.btn[i[0]][i[1]]["text"] = "X"
            self.btn[i[0]][i[1]]["bg"] = "red"
        messagebox.showinfo("", "END")
        self.root.destroy()
            

    def opendfs(self, x, y):
        if self.check(x, y) == 0:
            return
        btntmp = self.btn[x][y]
        if self.mapp[x][y] > 0 and btntmp['text'] == "":
            btntmp["text"] = self.mapp[x][y]
            btntmp["bg"] = "white"
            return
        elif self.mapp[x][y] == 0 and btntmp["bg"] == "grey":
            btntmp["bg"] = "white"
            for i in range(8):
                self.opendfs(x + self.dx[i], y + self.dy[i])
        return


    def autoopen(self, x, y):
        cnt = 0
        tmp = []
        for i in range(8):
            if self.check(x + self.dx[i], y + self.dy[i]) == 0:
                continue
            elif self.btn[x + self.dx[i]][y + self.dy[i]]["text"] == "*" :
                cnt += 1
            elif self.btn[x + self.dx[i]][y + self.dy[i]]["text"] == "" and self.btn[x + self.dx[i]][y + self.dy[i]]["bg"] == "grey":
                tmp.append([x + self.dx[i], y + self.dy[i]])
        if cnt == self.mapp[x][y]:
            for i in tmp:
                self.click(i[0], i[1])
        return
    
    
    def checkwin(self):
        for i in self.marklist:
            if not(i in self.bombs):
                self.end()
        messagebox.showinfo("", "WIN!")
        self.root.destroy()



if __name__ == '__main__':
    xx, yy, bomb = 10, 10, 10
    game = Saolei(xx, yy, bomb)
    game.root.mainloop()