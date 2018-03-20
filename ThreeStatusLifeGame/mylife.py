# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 21:13:18 2017

@author: Owner
"""

import wx
import copy
from numpy import random


ROW_NUM = 40
COL_NUM = 40
DEAD = 0
ALIVE = 1
WALL = 2
STATUS = [DEAD, ALIVE, WALL]
STATUS_COLOUR = [wx.WHITE, wx.GREEN, wx.BLACK]


class GridPanel(wx.Panel):
    def __init__(self, parent, LifeItems, id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)
        # self.SetBackgroundColour("WHITE")
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.items = LifeItems
        self.dc = wx.WindowDC(self)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouce)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_makewall)
        self.RunFlag = 0


    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        #print(w,h)
        self.dc.Clear()
        self.ItemPaint()

    def ItemPaint(self):
        w, h = self.GetClientSize()
        x_size = w / COL_NUM
        y_size = h / ROW_NUM
        for i in range(ROW_NUM):
            for j in range(COL_NUM):
                self.PaintGrid(i, j, x_size, y_size)
        # print("draw")

    def PaintGrid(self, row, col, x_size, y_size):
        c = STATUS_COLOUR[self.items.GetLife(row, col)]
        self.dc.SetPen(wx.Pen(wx.LIGHT_GREY))
        self.dc.SetBrush(wx.Brush(c))
        self.dc.DrawRectangle(col * x_size, row * y_size, x_size, y_size)
       

    def NextPaint(self):
        self.items.Change()
        self.ItemPaint()

    def SetRandom(self, event):
        print("push random")
        if not self.RunFlag:
            print("random")
            for i in range(ROW_NUM):
                for j in range(COL_NUM):
                    self.items.items[i][j].SetRandom()
            self.ItemPaint()
        else:
            print("can't random")

    def SetInit(self, event):
        print("push reset")
        if not self.RunFlag:
            print("reset")
            for i in range(ROW_NUM):
                for j in range(COL_NUM):
                    self.items.items[i][j].SetInit()
            self.ItemPaint()
        else:
            print("can't reset")

    def on_makewall(self, event):
        print("make wall")
        if not self.RunFlag:
            mx, my = event.GetPosition()
            px, py = self.GetClientSize()
            itemx, itemy = px/ROW_NUM, py/COL_NUM
            i, j = int(my/itemy), int(mx/itemx)
            print("make wall from (" + str(i)+","+str(j)+")")
            self.items.items[i][j].ChangeStatus(WALL)
            self.items.items[i][j].SetStatus()
            self.ItemPaint()
        else:
            print("can't make wall")


    def on_mouce(self, event):
        print("push mouce to change")
        if not self.RunFlag:
            #print(event.GetPosition())
            mx, my = event.GetPosition()
            px, py = self.GetClientSize()
            itemx, itemy = px/ROW_NUM, py/COL_NUM
            i, j = int(my/itemy), int(mx/itemx)
            print("change(" + str(i)+","+str(j)+")")
            life = self.items.GetLife(i, j)
            if life == DEAD:
                self.items.items[i][j].ChangeStatus(ALIVE)
            elif life == ALIVE:
                self.items.items[i][j].ChangeStatus(DEAD)
            else:
                self.items.items[i][j].ChangeStatus(DEAD)
            self.items.items[i][j].SetStatus()
            self.ItemPaint()
        else:
            print("can't change")

    def on_NextPaint(self, event):
        print("push step")
        if not self.RunFlag:
            print("step")
            self.NextPaint()
        else:
            print("can't step")

class Life:
    def __init__(self, Status):
        self.life = Status
        self.nextlife = Status

    def ChangeStatus(self, Status):
        # 状態を０か１で設定しているためこのようにできる
        self.nextlife = Status
        
    def NoChange(self):
        self.nextlife = copy.copy(self.life)

    def SetStatus(self):
        self.life = copy.copy(self.nextlife)

    def SetRandom(self):
        self.life = random.choice(STATUS, p=[0.49, 0.49, 0.02])

    def SetInit(self):
        self.life = DEAD


class LifeItems:
    def __init__(self):
        self.items = [[Life(DEAD) for j in range(COL_NUM)] for i in range(ROW_NUM)]

    def Change(self):
        # ライフゲームのルール記述部分
        for i in range(ROW_NUM):
            for j in range(COL_NUM):
                c0, c1, c2 = self.Count(i, j)
                life = self.GetLife(i, j)
                if life == DEAD:
                    if c1==3:
                        self.items[i][j].ChangeStatus(ALIVE)
                    else:
                        self.items[i][j].NoChange()
                elif life == ALIVE:
                    if c1<=1 or c1>=4:
                        self.items[i][j].ChangeStatus(DEAD)
                    else:
                        self.items[i][j].NoChange()
                else:
                    self.items[i][j].NoChange()
                #print(c)
        self.NextLife()

    def NextLife(self):
        for i in range(ROW_NUM):
            for j in range(COL_NUM):
                self.items[i][j].SetStatus()

    def GetLife(self, row, col):
        return self.items[row][col].life

    def Count(self, row, col):
        count0 = 0
        count1 = 0
        count2 = 0
        #print("DoA\trow\tcol\tnum")
        #print(str(self.GetLife(row, col))+"\t"+str(row)+"\t"+str(col), end="\t")
        for i in range(-1, 2):
            for j in range(-1, 2):
                # print(i, j)
                if i==0 and j==0:
                    continue
                if row+i<0 or col+j<0 or row+i>=ROW_NUM or col+j>=COL_NUM:
                    continue
                life =  self.GetLife(row+i, col+j)
                if life == DEAD:
                    count0+=1
                elif life == ALIVE:
                    count1+=1
                else:
                    count2+=1
                # print(row+i, col+j)
        return count0, count1, count2


class LifeFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size=(500, 600))
        self.Center()
        self.SetTitle(u"ライフゲーム")
        print("="*30)
        print("")
        print(str(ROW_NUM)+"x"+str(COL_NUM))


        # フレームのベース
        base = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)
        base.SetSizer(layout)

        # ライフゲームのパネル
        Items = LifeItems()
        self.gpanel = GridPanel(base, Items)
        layout.Add(self.gpanel, flag=wx.EXPAND | wx.ALL, border=5, proportion=1)

        # 下半分のボタン群用の設定
        hlayout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(hlayout, flag=wx.EXPAND)
        # 実行用のボタン
        run_btn = wx.Button(base, label="start")
        run_btn.Bind(wx.EVT_BUTTON, self.ChangeLabel)
        hlayout.Add(run_btn, proportion=1)
        # ステップ実行用のボタン
        step_btn = wx.Button(base, label="step")
        step_btn.Bind(wx.EVT_BUTTON, self.gpanel.on_NextPaint)
        hlayout.Add(step_btn, proportion=1)
        # ランダム設置用のボタン
        rand_btn = wx.Button(base, label="random")
        rand_btn.Bind(wx.EVT_BUTTON, self.gpanel.SetRandom)
        hlayout.Add(rand_btn, proportion=1)
        # リセット用のボタン
        reset_btn = wx.Button(base, label="reset")
        reset_btn.Bind(wx.EVT_BUTTON, self.gpanel.SetInit)
        hlayout.Add(reset_btn, proportion=1)

        self.Show()

    def ChangeLabel(self, event):
        # フラグが経っている間は実行できるようにしたい
        window = event.GetEventObject()
        if not self.gpanel.RunFlag:
            self.gpanel.RunFlag = 1
            print("push start")
            window.SetLabel("stop")
        else:
            self.gpanel.RunFlag = 0
            print("push stop")
            window.SetLabel("start")
        self.Paint()

    def Paint(self):
        print("paint")
        if self.gpanel.RunFlag:
            print("paint if")
            self.gpanel.NextPaint()
            wx.CallLater(100, self.Paint)


app = wx.App(True, "log.txt")
frame = LifeFrame()
app.MainLoop()
