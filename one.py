#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk,messagebox,simpledialog,filedialog
from tkinter import *
import subprocess
import store
import fnmatch
import os
import logging
from PopPages import NewFileInputPage
from threading import Thread
from time import sleep, ctime

#用于通信的类，主要保存用户输入的新建项目的信息(精华所在)
class data():
    def __init__(self):
        self.flage=0
        self.info=[]


class MainWindow:
    def __init__(self):
        #----------------------------------保存信息-----------------------------------------
        self.newFileInfo=[]


        #-----------------------------------页面布局-----------------------------------------
        self.root = Tk()
        self.root.title("固件分析平台")
        self.root.geometry("900x600")


        self.menubar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="新建项目", command=self.new_project_click)
        self.file_menu.add_command(label="打开")
        self.file_menu.add_command(label="打开最近的文件")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="保存")
        self.file_menu.add_command(label="另存为")
        self.file_menu.add_command(label="导出分析结果")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="开始分析")
        self.file_menu.add_command(label="退出", command=self.root.quit)


        self.menubar.add_cascade(label="文件", menu=self.file_menu)

        self.editmenu = Menu(self.menubar,tearoff=0)
        self.editmenu.add_command(label="配置文件", command=self.thirdpage)
        self.editmenu.add_command(label="开始")
        self.editmenu.add_command(label="暂停/继续")
        self.menubar.add_cascade(label="编辑", menu=self.editmenu)

        self.helpmenu = Menu(self.menubar,tearoff=0)
        self.helpmenu.add_command(label="说明文档")
        self.menubar.add_cascade(label="帮助", menu=self.helpmenu)

        self.root.config(menu=self.menubar)

        self.frame_left_top = Frame(self.root, width=200, height=400)
        self.frame_center_top = Frame(self.root, width=700, height=400)
        self.frame_left_bottom = Frame(self.root, width=600, height=300)
        self.frame_right_bottom = Frame(self.root, width=200, height=300)


    # 定义左上方项目栏
        self.left_top_title = Label(self.frame_left_top, text="项目")
        self.left_top_title.place(x=80, y=0, anchor='nw')

        # self.listbox = tk.Listbox(self.frame_left_top, height=23)
        # # # self.listbox.grid(row=1, column=0, columnspan=2, sticky=NSEW)
        # self.listbox.place(x=0, y=20, anchor='nw')

        #项目栏的树形窗口
        self.treeview = tk.ttk.Treeview(self.frame_left_top, height=100)
        self.treeview.place(x=0, y=20,anchor='nw')
        self.treeview.bind('<Button-3>', self.add_analysis)

        self.popmenu = Menu(self.root, tearoff=0)
        self.popmenu.add_command(label="导入固件", command=self.uploadaction)
        self.popmenu.add_command(label="开始分析", command=self.start)
        self.popmenu.add_command(label="配置信息", command=self.thirdpage)

    # 定义中上方项目信息栏

        # frame1:普通项目窗口
        frame1 = Frame(self.frame_center_top, width=700, height=400)
        frame1.place(x=0, y=0)
        frame1_title = Label(frame1, text='项目信息' )
        frame1_title.place(x=320, y=0)
        self.frame1 = frame1

        tree1 = ttk.Treeview(frame1, show="headings", height=18, columns=("a", "b", "c", "d", "e"))
        vbar1 = ttk.Scrollbar(frame1, orient=VERTICAL, command=tree1.yview)
        # 定义树形结构与滚动条
        tree1.configure(yscrollcommand=vbar1.set)

        # 表格的标题
        tree1.column("a", width=50, anchor="center")
        tree1.column("b", width=200, anchor="center")
        tree1.column("c", width=200, anchor="center")
        tree1.column("d", width=100, anchor="center")
        tree1.column("e", width=150, anchor="center")
        tree1.heading("a", text="编号")
        tree1.heading("b", text="项目名")
        tree1.heading("c", text="添加时间")
        tree1.heading("d", text="已分析/固件数")
        tree1.heading("e", text="打开项目文件夹")

        tree1.place(x=0, y=20, anchor='nw')
        vbar1.place(x=685, y=20, anchor='nw')

        # 调用方法获取表格内容插入

        #初始化表格
        # self.initInfo()

        # frame2具体项目内固件信息列表
        frame2 = Frame(self.frame_center_top, relief="sunken", width=700, height=400)
        frame2.place(x=0, y=0)
        frame2_title = Label(frame2, text='项目详情')
        frame2_title.place(x=320, y=0)
        self.frame2 = frame2

        tree2 = ttk.Treeview(frame2, show="headings", height=18, columns=("a", "b", "c", "d", "e"))
        vbar2 = ttk.Scrollbar(frame2, orient=VERTICAL, command=tree2.yview)
        tree2.configure(yscrollcommand=vbar2.set)

        tree2.column("a", width=50, anchor="center")
        tree2.column("b", width=200, anchor="center")
        tree2.column("c", width=200, anchor="center")
        tree2.column("d", width=100, anchor="center")
        tree2.column("e", width=150, anchor="center")
        tree2.heading("a", text="编号")
        tree2.heading("b", text="固件名")
        tree2.heading("c", text="添加时间")
        tree2.heading("d", text="分析状态")
        tree2.heading("e", text="报告下载")

        tree2.place(x=0, y=20, anchor='nw')
        vbar2.place(x=685, y=20, anchor='nw')

        # frame3配置信息列表
        frame3 = Frame(self.frame_center_top, width=700, height=400)
        frame3.place(x=0, y=0)
        frame3_title = Label(frame3, text='配置信息')
        frame3_title.place(x=320, y=0)
        self.frame3 = frame3

        CheckVar1 = IntVar()
        CheckVar2 = IntVar()
        CheckVar3 = IntVar()
        CheckVar4 = IntVar()
        CheckVar5 = IntVar()
        CheckVar6 = IntVar()
        CheckVar7 = IntVar()
        CheckVar8 = IntVar()
        CheckVar9 = IntVar()
        CheckVar10 = IntVar()
        CheckVar11 = IntVar()
        CheckVar12 = IntVar()
        CheckVar13 = IntVar()
        CheckVar14 = IntVar()
        CheckVar15 = IntVar()
        CheckVar16 = IntVar()
        CheckVar17 = IntVar()
        CheckVar18 = IntVar()
        CheckVar19 = IntVar()
        CheckVar20 = IntVar()
        CheckVar21 = IntVar()
        CheckVar22 = IntVar()

        ch1 = Checkbutton(frame3, text='固件基本分析', variable=CheckVar1, onvalue=1, offvalue=0)
        ch2 = Checkbutton(frame3, text='系统检测', variable=CheckVar2, onvalue=1, offvalue=0)
        ch3 = Checkbutton(frame3, text='静态二进制文件版本检测', variable=CheckVar3, onvalue=1,offvalue=0)
        ch4 = Checkbutton(frame3, text='关键函数检测', variable=CheckVar4, onvalue=1, offvalue=0)
        ch5 = Checkbutton(frame3, text='二进制安全机制检测', variable=CheckVar5, onvalue=1, offvalue=0)
        ch6 = Checkbutton(frame3, text='敏感函数检测', variable=CheckVar6, onvalue=1, offvalue=0)
        ch7 = Checkbutton(frame3, text='Bootloader和系统启动项检测', variable=CheckVar7, onvalue=1,offvalue=0)
        ch8 = Checkbutton(frame3, text='脚本文件安全检测', variable=CheckVar8, onvalue=1, offvalue=0)
        ch9 = Checkbutton(frame3, text='内核检测', variable=CheckVar9, onvalue=1, offvalue=0)
        ch10 = Checkbutton(frame3, text='Web文件检测', variable=CheckVar10, onvalue=1, offvalue=0)
        ch11 = Checkbutton(frame3, text='文件权限安全检测', variable=CheckVar11, onvalue=1, offvalue=0)
        ch12 = Checkbutton(frame3, text='密码文件检测', variable=CheckVar12, onvalue=1, offvalue=0)
        ch13 = Checkbutton(frame3, text='用户、组和验证检测', variable=CheckVar13, onvalue=1, offvalue=0)
        ch14 = Checkbutton(frame3, text='证书检测', variable=CheckVar14, onvalue=1, offvalue=0)
        ch15 = Checkbutton(frame3, text='配置文件检测', variable=CheckVar15, onvalue=1, offvalue=0)
        ch16 = Checkbutton(frame3, text='敏感二进制文件检测', variable=CheckVar16, onvalue=1, offvalue=0)
        ch17 = Checkbutton(frame3, text='grepit扫描检测', variable=CheckVar17, onvalue=1, offvalue=0)
        ch18 = Checkbutton(frame3, text='yara代码模块检测', variable=CheckVar18, onvalue=1, offvalue=0)
        ch19 = Checkbutton(frame3, text='Qemu仿真测试', variable=CheckVar19, onvalue=1, offvalue=0)
        ch20 = Checkbutton(frame3, text='动态二进制文件版本检测', variable=CheckVar20, onvalue=1,offvalue=0)
        ch21 = Checkbutton(frame3, text='许可证扫描', variable=CheckVar21, onvalue=1, offvalue=0)
        ch22 = Checkbutton(frame3, text='版本漏洞扫描', variable=CheckVar22, onvalue=1, offvalue=0)

        ch1.place(x=35, y=25)
        ch2.place(x=235, y=25)
        ch3.place(x=435, y=25)
        ch4.place(x=35, y=55)
        ch5.place(x=235, y=55)
        ch6.place(x=435, y=55)
        ch7.place(x=35, y=85)
        ch8.place(x=235, y=85)
        ch9.place(x=435, y=85)
        ch10.place(x=35, y=115)
        ch11.place(x=235, y=115)
        ch12.place(x=435, y=115)
        ch13.place(x=35, y=145)
        ch14.place(x=235, y=145)
        ch15.place(x=435, y=145)
        ch16.place(x=35, y=175)
        ch17.place(x=235, y=175)
        ch18.place(x=435, y=175)
        ch19.place(x=35, y=205)
        ch20.place(x=235, y=205)
        ch21.place(x=435, y=205)
        ch22.place(x=35, y=235)

    # 定义左下方分析进程栏
        self.left_bottom_title = Label(self.frame_left_bottom, text="分析进度")
        self.left_bottom_title.place(x=10, y=0, anchor='nw')

        self.left_bottom_text = Text(self.frame_left_bottom, width=200, height=8)
        self.left_bottom_text.place(x=10, y=20, anchor='nw')

    # ------------------------------------定义右下方按钮-----------------------------------------------------------#
    #     self.right_top_title = Label(self.frame_right_bottom, text='分析配置')
    #     # self.right_top_title.grid(row=0, column=0, sticky=NSEW)
    #     self.right_top_title.place(x=10, y=10, anchor='nw')
        self.btn1 = Button(self.frame_right_bottom, text="开始分析", width=10, height=2)
        self.btn1.place(x=120, y=10, anchor='nw')

        self.btn3 = Button(self.frame_right_bottom, text="选择配置", width=10, height=2, command=self.thirdpage)
        self.btn3.place(x=20, y=10, anchor='nw')

        self.btn2 = Button(self.frame_right_bottom, text="查看报告", width=10, height=2)
        self.btn2.place(x=20, y=80, anchor='nw')

        self.btn4 = Button(self.frame_right_bottom, text="显示所有项目", width=10, height=2, command=self.firstpage)
        self.btn4.place(x=120, y=80, anchor='nw')



        self.frame_left_top.place(x=0, y=0)
        self.frame_center_top.place(x=200, y=0)
        self.frame_left_bottom.place(x=0, y=400)
        self.frame_right_bottom.place(x=600, y=400)

        self.frame2.tkraise()


        # 将日志输出到 Text 控件中
        # self.bottom_text.insert(tk.END, handler.stream.getvalue())

        # 定时更新日志
        # self.root.after(1000, update_log)


        self.root.mainloop()



# #---------------------------------------------------------------------------------------------------------------#
#     # 初始化表格
#     def initInfo(self,onlytable = 0):
#         if onlytable == 0:
#             # 初始化左边树状view
#             fathers, childrens = store.getTreeView()
#             if len(childrens)!=0:
#                 for i, father in enumerate(fathers):
#                     temp = self.treeview.insert('', 'end', text=father)
#                     for children in childrens:
#                         if children[-1] == father:
#                             tempchildren=self.treeview.insert(temp, 'end', text=children[1],values=children[0])
#                             #添加双击事件
#                             self.treeview.bind('<Double-1>',self.doubleOne)
#
#          # data = [['1', 2, 3, 4, 5], [1, 2, 3, 4, 5]]
#         for i in self.tree1.get_children():
#             self.tree1.delete(i)
#         data = store.readInfo()
#         i = 0
#         for v in data:
#             v.insert(0, i + 1)  # 第一列的显示内容(序号)
#             self.tree1.insert('', i, values=(v))
#             i += 1
#
#         # 更新和保存treeview
#
#     def saveTreeView(self, name, fathername,gujianpath,downfilepath=''):
#         id=store.storeInfo(name, fathername, gujianpath=gujianpath,downfilepath=downfilepath)
#         return id
#
    #新建项目
    #点击新建文件跳到此函数
    def new_project_click(self):
        # # 获取当前选中的节点
        # current_node = ''
        # # project_name = simpledialog.askstring("新建项目", "请输入项目名称：", parent=self.root)
        # #project_name = f'{self.treeview.item(current_node)["text"]}_{len(self.treeview.get_children(current_node)) + 1}'
        # self.treeview.insert(current_node, 'end', text=project_name, values=('项目信息', '分析配置', '分析进程'))

        #创建通信对象
        data1=data()
        #开一个线程去监听里面的标志是否改变
        t1=Thread(target=self.monitordata, args=(data1,))
        t1.start()  #启动线程
        g1=NewFileInputPage(data1)
        g1.start()   #弹出新的进程页面，让用户输入信息，同时将通信对象data1传进去(传递的引用)


    #监听通信对象
    def monitordata(self,data1):
        #标志没变就一直等待
        while(data1.flage==0):
            continue
        #到这里必定能拿到信息
        self.newFileInfo=data1.info
        print(self.newFileInfo)





    def add_analysis(self,event):
        # 获取当前选中的节点
        current_node = self.treeview.identify_row(event.y)
        print(current_node)

        # 如果当前选中的是项目节点，则在该项目节点下创建新的分析
        if current_node and not self.treeview.get_children(current_node):
            self.popmenu.post(event.x_root, event.y_root)
        else:
            if self.treeview.get_children(current_node):
                self.popmenu.post(event.x_root, event.y_root)
            else:
                messagebox.showerror('错误', '请选择项目节点进行添加！')
        # 如果当前选中的是分析节点，则在该节点的父节点下创建新的分析
        # elif current_node and self.treeview.parent(current_node):
        #     analysis_name = f'{self.treeview.item(current_node)["text"]}_{len(self.treeview.get_children(self.treeview.parent(current_node))) + 1}'
        #     self.treeview.insert(self.treeview.parent(current_node), 'end', text=analysis_name)
        # else:
        #     messagebox.showerror('错误', '请选择项目节点或分析节点进行添加！')
#
#
#
#     def callback(self):
#         pass
#
    def uploadaction(self):
        current_node = self.treeview.focus()
        global filename
        filename = filedialog.askopenfilename()
        self.treeview.bind("<Double-1>", self.showInfo)
        if filename and not os.path.isdir(filename):
            truename=os.path.basename(filename)
            #向txt中添加记录
            father_name=self.treeview.item(current_node,'text')
            id=self.saveTreeView(truename,father_name,filename)
            #添加新的
            temp=self.treeview.insert(current_node, 'end', text=truename,values=id)
            #刷新数据
            self.initInfo(onlytable=1)
            #temp.bind("<Double-1>", self.print)
        else:
            messagebox.showerror('错误', '请选择一个文件！')
#
#     def showInfo(self,dd):
#         print(dd)
#         current_node = self.treeview.focus()
#         print(current_node)
#
    def start(self):
        current_node = self.treeview.focus()
        id=self.treeview.item(current_node,'value')[0]
        filename=self.treeview.item(current_node,'text')[:4]
        _,datas= store.getTreeView()
        jujianpath=''
        for data in datas:
            if data[0] == id:
                jujianpath = data[5]
                break
        # 执行命令脚本
        log_path = "/home/kali/Downloads/log1"
        profile_path = "./scan-profiles/default-scan.emba"
        # logging.basicConfig(filename='mylogger', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
        # cmd_log = open(Log_path, "w")
        cmd = 'sudo ./emba.sh -l '+ log_path +' -f ' + jujianpath + ' -p ' + profile_path

        # subprocess.Popen(["sudo", "./emba.sh", "-l", log_path, "-f", file_path, "-p", profile_path], shell=False,
        #                  stdout=cmd_log)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 创建日志对象
        # logger = logging.getLogger('mylogger')
        # logger.setLevel(logging.DEBUG)
        p.wait()


        path = r'/home/kali/Downloads/'
        openname=''
        for file_name in os.listdir(path):
            if file_name[0:7]=='result_':
                if file_name[7:11]==filename:
                    openname=file_name
                    break
        downpath='home/kali/Downloads/'+openname+'/'
        store.updateInfo(id,downpath)
        self.initInfo(1)
#
#     #双击事件
#     def doubleOne(self,info):
#         current_node = self.treeview.focus()
#         #如果有孩子就不是叶子结点，不管
#         if self.treeview.get_children(current_node):
#             return
#         id=self.treeview.item(current_node,'value')[0]
#         print(id)
#         for i in self.tree.get_children():
#             self.tree.delete(i)
#         _,datas= store.getTreeView()
#         print(id)
#         data1=[]
#         for data in datas:
#             if data[0]==id:
#                 data1=data
#                 break
#         data1[0]=data1[1:]
#         i = 0
#         print(data1)
#         for v in data1:
#             v.insert(0, i + 1)  # 第一列的显示内容(序号)
#             self.tree.insert('', i, values=(v))
#             i += 1

    # 下面三个函数判定项目信息栏显示在最外侧窗口是哪个模块
    def firstpage(self):
        if self.frame1.winfo_ismapped():
            print('1')
        elif self.frame2.winfo_ismapped():
            self.frame2.lower()
        elif self.frame3.winfo_ismapped():
            self.frame3.lower()
        self.frame1.tkraise()
        self.frame1.lift()

    def secondpage(self):
        if self.frame2.winfo_ismapped():
            print('2')
        elif self.frame1.ismapped():
            self.frame1.lower()
        elif self.frame3.winfo_ismapped():
            self.frame3.lower()
        self.frame2.tkraise()
        self.frame2.lift()

    def thirdpage(self):
        if self.frame3.winfo_ismapped():
            print('3')
        elif self.frame1.ismapped():
            self.frame1.lower()
        elif self.frame2.winfo_ismapped():
            self.frame2.lower()
        self.frame3.tkraise()
        self.frame3.lift()

MainWindow()
