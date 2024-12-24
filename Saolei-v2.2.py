'''
2024.10.22
于习概课
'''

from random import randint
from tkinter import *
from tkinter import messagebox

class Saolei:
    def __init__(self, xx, yy, bomb) -> None:
        """初始化"""
        self.xx = xx
        self.yy = yy
        self.bombnum = bomb

        self.dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        self.dy = [-1, 0, 1, -1, 1, -1, 0, 1]

        self.isstart = 0
        self.mark = 0
        self.root = Tk()
        self.root.title("SLGame@LZH")

        self.btn = [[None for _ in range(self.yy)] for _ in range(self.xx)]
        self.mapp = [[0 for _ in range(self.yy)] for _ in range(self.xx)]
        self.marklist = []
        self.guiinit()
        self.setbomb()


    def guiinit(self):
        """gui初始化"""
        for x in range(self.xx):
            for y in range(self.yy):
                btntmp = Button(self.root, width = 2, height = 1, bg = "grey", command = lambda x0 = x, y0 = y : self.click(x0, y0))
                btntmp.bind("<Button-3>", lambda event, x0 = x, y0 = y : self.rightclick(x0, y0))
                btntmp.grid(row=x, column=y)
                self.btn[x][y] = btntmp
        restart_btn = Button(self.root, text = "Restart", command = self.restart)
        restart_btn.grid(row=self.xx, column=0, columnspan=3)

        quit_btn = Button(self.root, text = "Quit", command = self.quit)
        quit_btn.grid(row=self.xx, column=4, columnspan=2)

        setting_btn = Button(self.root, text="Settings", command=self.settings)
        setting_btn.grid(row=self.xx, column=7, columnspan=3)

        self.lable = Label(self.root, text=f"Flagcnt: {self.mark}, Bomb: {self.bombnum}")
        self.lable.grid(row=self.xx+1, columnspan=10)

    def setbomb(self):
        """放置雷"""
        self.bombs = []
        self.mapp = [[0 for _ in range(self.yy)] for _ in range(self.xx)]
        while len(self.bombs) < self.bombnum:
            x0 = randint(0, self.xx - 1)
            y0 = randint(0, self.yy - 1)
            if self.mapp[x0][y0] == 0:
                self.mapp[x0][y0] = -1
                self.bombs.append([x0, y0])
        for x in range(self.xx):
            for y in range(self.yy):
                if self.mapp[x][y] == -1:
                    for i in range(8):
                        if self.check(x+self.dx[i], y+self.dy[i]) and self.mapp[x+self.dx[i]][y+self.dy[i]] != -1 :
                            self.mapp[x+self.dx[i]][y+self.dy[i]] += 1
    

    def click(self, x, y):
        """按button"""
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
        """雷的标记"""
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
        
        self.lable["text"] = f"Flagcnt: {len(self.marklist)}, Bomb: {self.bombnum}"

        if len(self.marklist) == self.bombnum:
            self.checkwin()
    

    def start(self, x, y):
        """第一次按"""
        while(self.mapp[x][y] != 0):
            self.setbomb()
        
        self.isstart = 1
        self.mark = 0
        for i in range(self.xx):
            for j in range(self.yy):
                self.btn[i][j]["text"] = ""
                self.btn[i][j]["bg"] = "grey"


    def check(self, x, y) -> bool:
        """检测是否越界 1 / 0 """
        return 1 if 0 <= x < self.xx and 0 <= y < self.yy else 0
            

    def end(self):
        '''死了'''
        for i in self.bombs:
            self.btn[i[0]][i[1]]["text"] = "X"
            self.btn[i[0]][i[1]]["bg"] = "red"
        
        self.create_end_window()

    def create_end_window(self):
        self.end_window = Tk()

        Label(self.end_window, text="Lose!").grid(row=0)

        self.end_restart_button = Button(self.end_window, text="Restart", command=self.end_restart)
        self.end_restart_button.grid(row=1, column=0)

        self.end_setting_button = Button(self.end_window, text="Settings", command=self.end_settings)
        self.end_setting_button.grid(row=1, column=1)

        self.end_window.mainloop()
            
    def end_settings(self):
        self.end_window.destroy()
        self.settings()
        pass

    def end_restart(self):
        self.end_window.destroy()
        self.restart()
        pass

    def opendfs(self, x, y):
        '''自动打开空白方块'''
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


    def restart(self):
        self.guiinit()
        self.setbomb()
        self.isstart = 0
        self.marklist = []

    def quit(self):
        self.root.destroy()

    def settings(self):
        self.root.destroy()
        self.setting_window = Tk()

        Label(self.setting_window, text="X").grid(row=0)
        Label(self.setting_window, text="Y").grid(row=1)
        Label(self.setting_window, text="Bomb").grid(row=2)

        self.entry_x = Entry(self.setting_window)
        self.entry_x.grid(row=0, column=1, padx=5, pady=10)
        self.entry_y = Entry(self.setting_window)
        self.entry_y.grid(row=1, column=1, padx=5, pady=10)
        self.entry_b = Entry(self.setting_window)
        self.entry_b.grid(row=2, column=1, padx=5, pady=10)

        self.confirm_button = Button(self.setting_window, text="Confirm", command=self.confirm)
        self.confirm_button.grid(row=3, columnspan=2)

        self.setting_window.mainloop()
        pass

    def confirm(self):
        x = int(self.entry_x.get())
        y = int(self.entry_y.get())
        b = int(self.entry_b.get())
        self.setting_window.destroy()
        self.__init__(x, y, b)
        pass


if __name__ == '__main__':
    xx, yy, bomb = 20, 20, 50
    game = Saolei(xx, yy, bomb)
    game.root.mainloop()