from random import randint
from tkinter import *


# (x, y)x行y列

dx = [-1, -1, -1, 0, 0, 1, 1, 1]
dy = [-1, 0, 1, -1, 1, -1, 0, 1]

# 行与列数
xx, yy, bnum = 0, 0, 0


# -1雷 0空 数字-雷个数
a = [[0 for _ in range(200)]for _ in range(200)]

btn = [[None for _ in range(200)]for _ in range(200)]

def printa():
    for i in range(xx):
        for j in range(yy):
            print(a[i][j], end=" ")
        print()

def randplace(x, y):
    """
    随机一个坐标
    """
    x0 = randint(0, x-1)
    y0 = randint(0, y-1)
    return [x0, y0]

def setbomb(x, y, bomb):
    """
    放置雷
    """
    while bomb > 0:
        print("-")
        tmp = randplace(x, y)
        # print(tmp)
        if a[tmp[0]][tmp[1]] == 0:
            a[tmp[0]][tmp[1]] = -1
            bomb -= 1
            print(tmp)
    return



def check(x, y) -> bool:
    """
    检查是否越界
    """
    return 1 if 0 <= x <= xx and 0 <= y <= yy else 0


def initnum(x, y):
    """
    创建初始数字
    """
    for i in range(xx):
        for j in range(yy):
            if a[i][j] == -1:
                for k in range(8):
                    if check(i+dx[k], j+dy[k]) and a[i+dx[k]][j+dy[k]] != -1 :
                        a[i+dx[k]][j+dy[k]] += 1
    return

def init():
    """
    初始化
    """
    setbomb(xx, yy, bnum)

    initnum(xx, yy)
    printa()
    return


def delete_btn(btn : Button):
    btn.destroy()
    return

def guiinit():
    """
    图形界面初始化
    """
    root.geometry(f"{xx*40}x{yy*40}")
    title = Label(root, text="SL")
    title.grid(row=0, column=0)
    for i in range(xx):
        for j in range(yy):
            btn[i][j] = Button(root, text=f"{i}, {j}", command=delete_btn(btn[1][1]))
            btn[i][j].grid(row=i, column=j)
    return

if __name__ == '__main__':
    xx, yy, bnum = 10, 10, 10
    init()

    root = Tk()

    guiinit()
    
    root.mainloop()
