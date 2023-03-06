#!/usr/bin/env python

import time  # python里的日期模块

#def readInfo():

def readInfo():
    # 文件路径
    filepath = 'Info.txt'
    data1=[]
    with open(filepath, 'r', encoding='utf-8') as file:
        data1 = file.readlines()
        print(data1)
    data=[]
    for d in data1:
        d=d.split(',')
        d[-1]=d[-1][:-1]
        d=d[1:-1]
        data.append(d)
    return data

#编号 固件名 添加时间  固件状态 报告下载  分析配置(14)
def storeInfo(name,fathername,gujianpath,downfilepath):

    id=getNextId()
    name=name
    state='0'
    downpath='c/:d'
    fathername=fathername

    # 文件路径
    filepath = 'Info.txt'
    # 打开文件
    file = open(filepath, 'a')
    #读取当前时间
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    # 写入数据
    file.writelines(id+','+name+','+now+','+state+','+downpath+','+gujianpath+','+fathername+'\n')
    # 刷新缓存
    file.flush()

    return id
# def updateInfo():
#     # 文件路径
#     filepath = 'Info.txt'
#     data1 = []
#     with open(filepath, 'r', encoding='utf-8') as file:
#         data1 = file.readlines()
#     data = []
#     for d in data1:
#         d = d.split(',')
#         d[-1] = d[-1][:-1]
#         data.append(d)
#
# updateInfo()

def getTreeView():
    # 文件路径
    filepath = 'Info.txt'
    data1 = []
    father=[]
    with open(filepath, 'r', encoding='utf-8') as file:
        data1 = file.readlines()
        print(data1)
    data = []
    for d in data1:
        d = d.split(',')
        d[-1] = d[-1][:-1]
        data.append(d)
        father.append(d[-1])
    father=set(father)
    return father,data

#获取下一个id
def getNextId():
    # 文件路径
    filepath = 'idstore.txt'
    with open(filepath, 'r', encoding='utf-8') as file:
        data1 = file.readlines()
        print(data1)
        data2=str(int(data1[0])+1)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(data2)
    return data1[0]
getNextId()

#getTreeView()
def updateInfo(id,downpath):
    # 文件路径
    filepath = 'Info.txt'
    data1 = []
    with open(filepath, 'r', encoding='utf-8') as file:
        data1 = file.readlines()
    data = []
    for d in data1:
        d = d.split(',')
        if d[0]==id:
            d[3] ='1'
            d[4]=downpath
        data.append(d)
