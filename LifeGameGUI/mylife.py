# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 21:13:18 2017

@author: Owner
"""

import wx
import copy
import random


ROW_NUM = 40
COL_NUM = 40
DEAD = 0
ALIVE = 1
STATUS = [DEAD, ALIVE]
STATUS_COLOUR = [wx.WHITE, wx.GREEN]


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
            if life == ALIVE:
                self.items.items[i][j].ChangeStatus(DEAD)
            else:
                self.items.items[i][j].ChangeStatus(ALIVE)
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
    def __init__(self, DorA):
        self.life = DorA
        self.nextlife = DorA
        
    def ChangeStatus(self, DorA):
        # 状態を０か１で設定しているためこのようにできる
        self.nextlife = DorA
        
    def NoChange(self):
        self.nextlife = copy.copy(self.life)

    def SetStatus(self):
        self.life = copy.copy(self.nextlife)
        
    def SetRandom(self):
        self.life = random.choice(STATUS)
        
    def SetInit(self):
        self.life = DEAD
        

class LifeItems:
    def __init__(self):
        self.items = [[Life(DEAD) for j in range(COL_NUM)] for i in range(ROW_NUM)]

    def Change(self):
        # ライフゲームのルールに従って変化を記述
        for i in range(ROW_NUM):
            for j in range(COL_NUM):
                c = self.Count(i, j)
                if self.GetLife(i, j):
                    if c <= 1 or c >= 4:
                        self.items[i][j].ChangeStatus(DEAD)
                    else:
                        self.items[i][j].NoChange()
                else:
                    if c == 3:
                        self.items[i][j].ChangeStatus(ALIVE)
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
        count = 0
        #print("DoA\trow\tcol\tnum")
        #print(str(self.GetLife(row, col))+"\t"+str(row)+"\t"+str(col), end="\t")
        # 普通のライフゲームのルールと違って一つ深く探る
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i==0 and j==0:
                    continue
                if row+i<0 or col+j<0 or row+i>=ROW_NUM or col+j>=COL_NUM:
                    continue
                count += self.GetLife(row+i, col+j)
                # print(row+i, col+j)
        return count


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
