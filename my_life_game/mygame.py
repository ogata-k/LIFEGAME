# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 11:52:43 2016

@author: Owner
"""
import random
import tkinter

# 生死を表す変数の定義
alive = 1
dead = 0
status = (dead, alive)

# 描画領域用の変数の定義とマスの準備
height = 30
width = 30
field = []

# 乱数の初期化
random.seed(0)

# マスの大きさとか色とかもろもろの定義
space = 5
cell = 16
color = {alive: "red", dead: "white"}
is_run = False


def draw():
    """
    外で作ったcanvasを描画する関数
    """
    canvas.delete("field")
    for i in range(height):
        for j in range(width):
            x0 = space + j * cell
            y0 = space + i * cell
            x1 = x0 + cell
            y1 = y0 + cell
            canvas.create_rectangle(x0, y0, x1, y1,
                                    fill=color[field[i][j]],
                                    tags="field")


def init():
    """
    外部のfield変数の初期化をして描画をする関数
    """
    for i in range(height):
        row = []
        for j in range(width):
            row.append(dead)
        field.append(row)
    draw()


def reset():
    """
    field変数の中身をすべてdeadにして描画する関数
    """
    if is_run:
        return

    for i in range(height):
        for j in range(width):
            field[i][j] = dead
    draw()


def rand_set():
    """
    fieldの中身をstatusの中からランダムに選択して配置する関数
    """
    if is_run:
        return

    for i in range(height):
        for j in range(width):
            field[i][j] = random.choice(status)
    draw()


def count(y, x):
    """
    field[y][x]の周辺のaliveなマスの数を数えて返す関数
    """
    num = 0

    if x != 0:
        num = num + field[y][x - 1]
        if y != 0:
            num = num + field[y - 1][x - 1]
        if y != height - 1:
            num = num + field[y + 1][x - 1]

    if x != width - 1:
        num = num + field[y][x + 1]
        if y != 0:
            num = num + field[y - 1][x + 1]
        if y != height - 1:
            num = num + field[y + 1][x + 1]

    if y != 0:
        num = num + field[y - 1][x]
    if y != height - 1:
        num = num + field[y + 1][x]

    return num


def next():
    """
    ライフゲームを進めていく関数で描画も行う
    """
    global field
    new_field = []
    for i in range(height):
        row = []
        for j in range(width):
            num = count(j, i)
            if num == 3:
                row.append(alive)
            elif num == 2:
                row.append(field[i][j])
            else:
                row.append(dead)
        new_field.append(row)
    field = new_field
    draw()


def run():
    """
    ライフゲームを500ミリ秒ごとに実行フラグが立っていないときに実行する関数
    """
    if is_run:
        next()
    root.after(500, run)


def start_stop():
    """
    ライフゲームを自動的に動かすかどうかのフラグを変更する関数
    """
    global is_run
    is_run = not is_run


def alive_dead(event):
    """
    マウスによって停止中のライフゲームのマスの生死を変更する関数
    """
    if is_run:
        return
    if event.x < space or event.x > (space + cell * width):
        return
    if event.y < space or event.y > (space + cell * height):
        return

    x = int((event.x - space) / cell)
    y = int((event.y - space) / cell)

    if field[y][x] == alive:
        field[y][x] = dead
    elif field[y][x] == dead:
        field[y][x] = alive

    draw()

root = tkinter.Tk()

# キャンバスやボタンを作成して配置する
canvas_h = space * 2 + height * cell
canvas_w = space * 2 + width * cell
canvas = tkinter.Canvas(root, width=canvas_w, height=canvas_h)
canvas.bind("<Button-1>", alive_dead)
canvas.pack()

reset_button = tkinter.Button(root, text="reset", command=reset)
reset_button.pack(side="left")

rand_button = tkinter.Button(root, text="rand", command=rand_set)
rand_button.pack(side="left")

run_button = tkinter.Button(root, text="start/stop", command=start_stop)
run_button.pack(side="left")

exit_button = tkinter.Button(root, text="exit", command=root.destroy)
exit_button.pack(side="right")

# 初期化→作動→Mainの繰り返し
init()
run()
root.mainloop()
