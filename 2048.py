"""
2048游戏
"""

from tkinter import *
from random import randint
from random import choice

class game:
    def __init__(self, xx, yy):
        '''初始化'''
        self.debug = 1
        self.dpi = 100
        self.xx = xx
        self.yy = yy
        self.board = [[0 for _ in range(self.yy)] for _ in range(self.xx)]
        self.score = 0

        self.dx = [-1, 1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.numlist = [2, 2, 2, 4]
        # 方块颜色字典
        self.color_dict = {
            2: "#ece4db",
            4: "#ebe0cb",
            8: "#e8b481",
            16: "#e89a6c",
            32: "#e68367",
            64: "#e46847",
            128: "#e8d07f",
            256: "#ffd700",
            # 512
            # 1024
            # 2048
        }

        self.startgame()
        pass

    def tr(self):
        '''矩阵转置'''
        self.board = [list(row) for row in zip(*self.board)]
        return
    
    def invert(self):
        '''矩阵反转'''
        self.board = [row[::-1] for row in self.board]
        return
    
    def guiinit(self):
        '''gui初始化'''
        self.root = Tk()
        self.root.title("2048")
        self.canvas = Canvas(self.root, height=self.xx*self.dpi, width=self.yy*self.dpi, bg="white")
        self.canvas.pack()
        self.root.bind("<Key>", self.key_pressed)
        if self.debug:
            print("guiinit")
        pass

    def color(self, point):
        '''返回一个对应点的颜色'''
        if self.color_dict.get(point) == None:
            return "grey"
        else:
            return self.color_dict[point]

    def draw_point(self, x, y, score):
        '''画一个点'''
        self.canvas.create_rectangle(y*self.dpi, x*self.dpi, (y+1)*self.dpi, (x+1)*self.dpi, outline="white", fill=self.color(score))
        self.canvas.create_text((y+0.5)*self.dpi, (x+0.5)*self.dpi, text=str(score), fill="white", justify="center", font=("Arial", 30))

    def draw(self):
        '''绘制所有点'''
        self.canvas.delete("all")
        for i in range(self.xx):
            for j in range(self.yy):
                point = self.board[i][j]
                if point != 0:
                    self.draw_point(i, j, point)
        if self.debug:
            print("draw")
        pass

    def randpoint(self):
        '''生成一个随机的坐标和数值'''
        x = randint(0, self.xx-1)
        y = randint(0, self.yy-1)
        num = choice(self.numlist)
        return [x, y, num]
    
    def creat_new_point(self):
        '''随机生成一个新点'''
        while 1:
            tmp = self.randpoint()
            if self.board[tmp[0]][tmp[1]] == 0:
                self.board[tmp[0]][tmp[1]] = tmp[2]
                if self.debug:
                    print("creat_new_point", tmp)
                return
        pass

    def check(self, x, y):
        return 1 if 0 <= x < self.xx and 0 <= y < self.yy else 0

    def check_lose(self):
        '''检测输没输'''
        print("check_lose")
        cnt = 0
        for i in range(self.xx):
            for j in range(self.yy):
                if self.board[i][j] != 0:
                    cnt += 1
        if cnt != self.xx * self.yy:
            return 0
        for i in range(self.xx):
            for j in range(self.yy):
                for k in range(4):
                    x1 = i + self.dx[k]
                    y1 = j + self.dy[k]
                    if self.check(x1, y1) == 0:
                        continue
                    else:
                        if self.board[x1][y1] == self.board[i][j]:
                            return 0
        return 1

    def move(self, x, y, dir: str):
        '''把(x, y)向dir方向移动'''
        moved = 0
        if dir == "Up":
            if x == 0:
                return moved
            while x > 0:
                if self.board[x-1][y] == 0:
                    self.board[x-1][y] = self.board[x][y]
                    self.board[x][y] = 0
                    x -= 1
                    moved = 1
                elif self.board[x-1][y] != 0 and self.board[x-1][y] != self.board[x][y]:
                    return moved
                elif self.board[x-1][y] == self.board[x][y]:
                    self.board[x-1][y] *= 2
                    self.board[x][y] = 0
                    moved = 1
                    return moved
                
        if dir == "Down":
            if x == self.xx - 1:
                return moved
            while x < self.xx - 1:
                if self.board[x+1][y] == 0:
                    self.board[x+1][y] = self.board[x][y]
                    self.board[x][y] = 0
                    x += 1
                    moved = 1
                elif self.board[x+1][y] != 0 and self.board[x+1][y] != self.board[x][y]:
                    return moved
                elif self.board[x+1][y] == self.board[x][y]:
                    self.board[x+1][y] *= 2
                    self.board[x][y] = 0
                    moved = 1
                    return moved
        return moved

    def key_pressed(self, event):
        direct = event.keysym
        if self.debug:
            print(f"Keypressed: {direct}")
        
        moved = 0

        if direct == "Up":
            for i in range(self.xx):
                for j in range(self.yy):
                    if self.board[i][j] != 0:
                        moved += self.move(i, j, direct)

        elif direct == "Down":
            for i in range(self.xx-1, -1, -1):
                for j in range(self.yy):
                    if self.board[i][j] != 0:
                        moved += self.move(i, j, "Down")

        elif direct == "Left":
            self.tr()
            for i in range(self.xx):
                for j in range(self.yy):
                    if self.board[i][j] != 0:
                        moved += self.move(i, j, "Up")
            self.tr()
            pass

        elif direct == "Right":
            self.tr()
            for i in range(self.xx-1, -1, -1):
                for j in range(self.yy):
                    if self.board[i][j] != 0:
                        moved += self.move(i, j, "Down")
            self.tr()

        print(f"moved_blocks = {moved}")
        if moved:
            self.creat_new_point()
            pass
        else:
            if self.check_blocks_full():
                if self.check_lose():
                    self.lose()

        self.draw()

        pass

    def startgame(self):
        self.guiinit()
        self.creat_new_point()
        self.creat_new_point()
        self.draw()


    def check_blocks_full(self) -> int:
        cnt = 0
        for i in range(self.xx):
            for j in range(self.yy):
                if self.board[i][j] != 0:
                    cnt += 1
        print("block_cnt =", cnt)
        if cnt == self.xx * self.yy:
            return 1
        else:
            return 0

    def lose(self):
        print("lose!")
        self.lose_window = Tk()
        self.lose_window.title("LOSE!")

        cnt = 0
        for i in range(self.xx):
            cnt += sum(self.board[i])
        Label(self.lose_window, text=f"SUM: {cnt}").pack()

        self.restart_btn = Button(self.lose_window, text="RESTART", command=self.restart)
        self.restart_btn.pack()
        self.lose_window.mainloop()
        pass


    def restart(self):
        self.root.destroy()
        self.lose_window.destroy()
        self.__init__(self.xx, self.yy)

if __name__ == '__main__':
    a = game(4, 4)
    a.root.mainloop()
    pass
