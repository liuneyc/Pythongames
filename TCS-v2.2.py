''''
2024.10.23
于现代工学通论
2024.10.24
更新：
1. 增加了设置功能
2. 增加了游戏结束功能

2024.10.27
更新：
1. 可以两条蛇共同游戏
'''

from random import randint
from tkinter import *

class TCSGame:
    def __init__(self, xx, yy, udt) -> None:
        """初始化"""
        self.xx = xx
        self.yy = yy

        self.isstart = 0

        self.snake1 = [[0, 0], [0, 1], [0, 2]]
        self.snake2 = [[self.xx-1, 0], [self.xx-1, 1], [self.xx-1, 2]]

        self.snake1_face = "Right"
        self.snake2_face = "d"
        self.score1 = 0
        self.score2 = 0
        self.stepcnt = 0

        self.food = [int(self.xx/2), int(self.yy/2)]

        self.update_time = udt
        # print(self.xx, self.yy, self.update_time)

        self.guiinit()
        self.root.bind("<Key>", self.key_pressed)
        self.snake_display()
        self.food_display()
        self.startgame()
        pass


    def rand_place(self):
        """返回一个随机坐标"""
        x0 = randint(0, self.xx - 1)
        y0 = randint(0, self.yy - 1)
        return [x0, y0]


    def guiinit(self):
        """gui初始化"""
        self.root = Tk()
        self.root.title("TCSGame@LZH")
        self.canvas0 = Canvas(self.root, height=self.xx*20, width=self.yy*20, bg="white")
        self.canvas0.pack()

        self.score_display = Label(self.root, text=f"Player1: {self.score1}  Player2: {self.score2}  Stepcnt: {self.stepcnt}")
        self.score_display.pack()
        
        self.setting_btn = Button(self.root, text="Settings", command=self.settings)
        self.setting_btn.pack()
        pass


    def snake_display(self):
        """"画蛇"""
        self.canvas0.delete("all")

        for i in self.snake1:
            self.canvas0.create_rectangle(i[1]*20, i[0]*20, i[1]*20+20, i[0]*20+20, fill="green")

        for i in self.snake2:
            self.canvas0.create_rectangle(i[1]*20, i[0]*20, i[1]*20+20, i[0]*20+20, fill="blue")
        pass
        

    def snake_update(self):
        '''更新游戏'''
        self.stepcnt += 1
        head1 = self.snake1[-1]
        head2 = self.snake2[-1]
        self.score_display["text"] = f"Player1: {self.score1}  Player2: {self.score2}  Stepcnt: {self.stepcnt}"
        if self.snake1_face == "Left":
            newhead1 = [head1[0], head1[1]-1]
        elif self.snake1_face == "Right":
            newhead1 = [head1[0], head1[1]+1]
        elif self.snake1_face == "Up":
            newhead1 = [head1[0]-1, head1[1]]
        elif self.snake1_face == "Down":
            newhead1 = [head1[0]+1, head1[1]]


        if self.snake2_face == "a":
            newhead2 = [head2[0], head2[1]-1]
        elif self.snake2_face == "d":
            newhead2 = [head2[0], head2[1]+1]
        elif self.snake2_face == "w":
            newhead2 = [head2[0]-1, head2[1]]
        elif self.snake2_face == "s":
            newhead2 = [head2[0]+1, head2[1]]


        if self.check_end(newhead1) or self.check_end(newhead2):# 输
            self.endgame()
        self.snake1.append(newhead1)
        self.snake2.append(newhead2)
        
        if newhead1 == self.food:
            self.score1 += 1
            while 1:
                foodtmp = self.rand_place()
                if (foodtmp not in self.snake1) and (foodtmp not in self.snake2):
                    self.food = foodtmp
                    break
        else:
            self.snake1.pop(0)
        
        if newhead2 == self.food:
            self.score2 += 1
            while 1:
                foodtmp = self.rand_place()
                if (foodtmp not in self.snake1) and (foodtmp not in self.snake2):
                    self.food = foodtmp
                    break
        else:
            self.snake2.pop(0)

        self.snake_display()
        self.food_display()

        self.root.after(self.update_time, self.snake_update)


    def food_display(self):
        '''画食物'''
        self.canvas0.create_oval(self.food[1]*20, self.food[0]*20, self.food[1]*20+20, self.food[0]*20+20, fill="red")


    def key_pressed(self, event):
        """绑定按键"""
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            self.snake1_face = event.keysym
        
        if event.keysym in ["a", "d", "w", "s"]:
            self.snake2_face = event.keysym
        pass


    def startgame(self):
        self.snake_update()
        pass


    def check_end(self, h):
        """检查是否结束"""
        if h[0] < 0 or h[1] < 0 or h[0] >= self.xx or h[1] >= self.yy or h in self.snake1 or h in self.snake2:
            return 1
        return 0


    def endgame(self):
        """结束界面"""
        self.end_window = Tk()
        self.end_window.title("输！")

        Label(self.end_window, text=f"Player1: {self.score1}  Player2: {self.score2}  Stepcnt: {self.stepcnt}").grid(row=0, columnspan=3)

        self.restart_btn = Button(self.end_window, text="Restart", command=self.restart)
        self.restart_btn.grid(row=1, column=0)

        self.end_setting_btn = Button(self.end_window, text="Settings", command=self.end_settings)
        self.end_setting_btn.grid(row=1, column=1)

        self.end_quit_btn = Button(self.end_window, text="Quit", command=self.end_quit)
        self.end_quit_btn.grid(row=1, column=2)

        self.end_window.mainloop()

    def end_settings(self):
        '''结束时按设置'''
        self.end_window.destroy()
        self.settings()
        pass

    def end_quit(self):
        '''结束时退出'''
        self.root.destroy()
        self.end_window.destroy()
        pass

    def settings(self):
        """设置界面"""
        self.root.destroy()

        self.setting_window = Tk()
        self.setting_window.title("Settings")
        Label(self.setting_window, text="X").grid(row=0)
        Label(self.setting_window, text="Y").grid(row=1)
        Label(self.setting_window, text="Update_Time(ms)").grid(row=2)

        self.entry_x = Entry(self.setting_window)
        self.entry_y = Entry(self.setting_window)
        self.entry_udtime = Entry(self.setting_window)

        self.entry_x.grid(row=0, column=1, padx=10, pady=5)
        self.entry_y.grid(row=1, column=1, padx=10, pady=5)
        self.entry_udtime.grid(row=2, column=1, padx=10, pady=5)
        
        self.cfmbtn = Button(self.setting_window, text="Confirm", command=self.confirm)
        self.cfmbtn.grid(row=3, columnspan=2)
        self.setting_window.mainloop()
        pass

    def confirm(self):
        """设置确认"""
        x = self.entry_x.get()
        y = self.entry_y.get()
        u = self.entry_udtime.get()

        x = int(x) if x != "" else self.xx
        y = int(y) if y != "" else self.yy
        u = int(u) if u != "" else self.update_time

        self.setting_window.destroy()
        self.__init__(x, y, u)
        pass

    def restart(self):
        """重新开始按钮"""
        self.end_window.destroy()
        self.root.destroy()
        self.__init__(self.xx, self.yy, self.update_time)
        pass



if __name__ == '__main__':
    xx, yy, udt = 20, 20, 100
    game = TCSGame(xx, yy, udt)
    game.root.mainloop()

    