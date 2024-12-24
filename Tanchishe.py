''''
2024.10.23
于现代工学通论
'''

from random import randint
from tkinter import *
from tkinter import messagebox

class TCSGame:
    def __init__(self, xx, yy) -> None:
        self.xx = xx
        self.yy = yy

        self.isstart = 0

        self.snake = [[0, 0], [0, 1], [0, 2]]
        self.snake_face = "Right"
        self.score = 0
        self.stepcnt = 0

        self.food = [5, 5]

        self.guiinit()
        self.root.bind("<Key>", self.key_pressed)
        self.snake_display()
        self.food_display()
        self.startgame()
        pass


    def rand_place(self):
        x0 = randint(0, self.xx - 1)
        y0 = randint(0, self.yy - 1)
        return [x0, y0]


    def guiinit(self):
        """
        gui初始化
        """
        self.root = Tk()
        self.root.title("TCSGame@LZH")
        self.canvas = Canvas(self.root, height=self.xx*20, width=self.yy*20)
        self.canvas.pack()
        self.score_display = Label(self.root, text=f"Score = {self.score}  Stepcnt = {self.stepcnt}")
        self.score_display.pack()
        pass


    def snake_display(self):
        """"
        显示蛇位置
        """
        self.canvas.delete("all")

        for i in self.snake:
            self.canvas.create_rectangle(i[1]*20, i[0]*20, i[1]*20+20, i[0]*20+20, fill="green")
        

    def snake_update(self):
        '''
        更新游戏
        '''
        head = self.snake[-1]
        self.stepcnt += 1
        self.score_display["text"] = f"Score = {self.score}  Stepcnt = {self.stepcnt}"
        if self.snake_face == "Left":
            newhead = [head[0], head[1]-1]
        elif self.snake_face == "Right":
            newhead = [head[0], head[1]+1]
        elif self.snake_face == "Up":
            newhead = [head[0]-1, head[1]]
        elif self.snake_face == "Down":
            newhead = [head[0]+1, head[1]]


        if self.checkend(newhead):# 输
            self.endgame()
        self.snake.append(newhead)
        if newhead == self.food:
            self.score += 1
            
            while 1:
                foodtmp = self.rand_place()
                if foodtmp not in self.snake:
                    self.food = foodtmp
                    break
        else:
            self.snake.pop(0)

        self.snake_display()
        self.food_display()


        self.root.after(100, self.snake_update)


    def food_display(self):
        '''
        显示食物
        '''
        self.canvas.create_oval(self.food[1]*20, self.food[0]*20, self.food[1]*20+20, self.food[0]*20+20, fill="red")


    def key_pressed(self, event):
        """
        绑定按键
        """
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            self.snake_face = event.keysym
        pass


    def startgame(self):
        self.snake_update()
        pass


    def checkend(self, h):
        if h[0] < 0 or h[1] < 0 or h[0] >= self.xx or h[1] >= yy or h in self.snake:
            return 1
        return 0

    def endgame(self):
        messagebox.showinfo("", f"END!\nScore = {self.score}")
        self.root.quit()


if __name__ == '__main__':
    xx, yy = 20, 20
    game = TCSGame(xx, yy)
    game.root.mainloop()