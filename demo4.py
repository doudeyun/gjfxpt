import tkinter as tk
from tkinter import *


class Index:
    def __init__(self):
        self.root = Tk()
        self.root.title("固件分析平台")
        self.root.geometry("900x600")

        self.frame_left = Frame(self.root, width=200, height=400)
        self.frame_right = Frame(self.root, width=700, height=400)

        self.frame_left.place(x=0, y=0)
        self.frame_right.place(x=200, y=0)

        # 三个按钮用于切换页面
        # for i in ["增加", "删除", "撤销"]:
        #     but = Button(self.frame_left, text=i)
        #     but.pack(side='top', expand=1, fill="y")
        #     but.bind("<Double-1>", self.change)

        self.btn1 = Button(self.frame_left, text="but1", width=10, height=2)
        self.btn1.place(x=90, y=10, anchor='nw')
        self.btn1.bind("<Double-1>", self.change)

        self.btn2 = Button(self.frame_left, text="but2", width=10, height=2)
        self.btn2.place(x=90, y=80, anchor='nw')
        self.btn2.bind("<Double-1>", self.change)

        self.btn3 = Button(self.frame_left, text="but3", width=10, height=2)
        self.btn3.place(x=90, y=150, anchor='nw')
        self.btn3.bind("<Double-1>", self.change)

            # 用于承载切换的页面内容

        lab = tk.Label(self.frame_right, text="我是第一个页面")
        lab.place(x=0, y=0)
        # 根据鼠标左键单击事件，切换页面

        self.root.mainloop()

    def change(self, event):
        res = event.widget["text"]
        for i in self.frame_right.winfo_children():
            i.destroy()
        if res == "but1":
            Page1(self.frame_right)
        elif res == "but2":
            Page2(self.frame_right)
        elif res == "but3":
            Page3(self.frame_right)


class Page1(tk.Frame):
    def __init__(self):
        # super().__init__(parent)
        # self.place(x=10, y=10)
        # tk.Label(self, text="配置选项").place(x=50, y=0, anchor='nw')
        #
        # self.CheckVar1 = IntVar()
        # ch1 = Checkbutton(self, text='固件基本分析', variable=self.CheckVar1, onvalue=1, offvalue=0)
        # ch1.place(x=5, y=5)

        self.place(x=300, y=110)
        tk.Label(self, text="配置选项").place(x=50, y=50, anchor='nw')

        # self.CheckVar1 = IntVar()
        # ch1 = Checkbutton(self, text='固件基本分析', variable=self.CheckVar1, onvalue=1, offvalue=0)
        # ch1.place(x=100, y=100)


# class Page2(tk.Frame):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.pack(expand=1, fill="both")
#         tk.Label(self, text="我是page2").pack()
#
#
# class Page3(tk.Frame):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.pack(expand=1, fill="both")
#         tk.Label(self, text="我是page3").pack()


if __name__ == "__main__":

    Index()

