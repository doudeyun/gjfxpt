import os
import sys
import time
import tkinter as tk
from tkinter import *
from threading import Thread
from time import sleep, ctime

from tkinter import filedialog
from tkinter.filedialog import askopenfilename
# from startcalendar import start_calendar
import datetime
#from tkcalendar import Calendar


#新建文件输出弹窗
class NewFileInputPage():
    def __init__(self,data):
        #Thread.__init__(self)  # 不要忘记调用Thread的初始化方法
        #通信对象
        self.data=data

        #页面布局
        self.root_window = tk.Tk()
        self.root_window.title('新建项目')
        self.root_window.geometry('630x330')

        self.lb1 = Label(self.root_window,text='项目名称',fg='black',font=('正楷',13),width=20,height=2)
        self.lb1.place(x=5, y=30)
        self.lb1_text = Text(self.root_window, width=20, height=2)
        self.lb1_text.place(x=140, y=35, anchor='nw')

        self.lb2 = Label(self.root_window,text='创建人',fg='black',font=('正楷',13),width=20,height=2)
        self.lb2.place(x=300, y=30)
        self.lb2_text = Text(self.root_window, width=20, height=2)
        self.lb2_text.place(x=435, y=35, anchor='nw')

        self.lb3 = Label(self.root_window, text='创建时间', fg='black', font=('正楷', 13), width=20, height=2)
        self.lb3.place(x=5, y=90)
        self.time1 = time.strftime('%Y-%m-%d')
        self.clock = Label(self.root_window, text=self.time1, font=28)
        self.clock.place(x=140, y=98)

        self.lb4 = Label(self.root_window,text='项目备注',fg='black',font=('正楷',13),width=20,height=2)
        self.lb4.place(x=5, y=150)
        self.lb4_text = Text(self.root_window, width=40, height=6)
        self.lb4_text.place(x=140, y=155, anchor='nw')

        self.btn1 = Button(self.root_window, text="确定", width=10, height=2, command=self.ok)
        self.btn1.place(x=150, y=270)

        self.btn2 = Button(self.root_window, text="取消", width=10, height=2, command=self.quit)
        self.btn2.place(x=350, y=270)

    #外部调用此函数，显示输入信息页面
    def start(self):
        self.root_window.mainloop()

    #点击确定
    def ok(self):
        #获取4个信息
        name=self.lb1_text.get('1.0', 'end')[:-1]
        person=self.lb2_text.get('1.0', 'end')[:-1]
        creattime=self.time1
        note=self.lb4_text.get('1.0', 'end')[:-1]
        self.info=[name,person,creattime,note]
        #改变通信对象的内容
        self.data.flage=1
        self.data.info=self.info
        #退出系统
        self.quit()

    #退出系统
    def quit(self):
        self.root_window.destroy()
    #返回输入的信息
    def getinfo(self):
        return self.info


#无任何实质功能，此语句作用:可以单独运行此文件，在其他脚本引入此脚本时，会忽略此语句
if __name__ == '__main__':
    NewFileInputPage().start()
