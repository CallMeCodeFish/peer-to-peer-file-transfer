#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-24-19 00:17
# pquery.py
# theme: PQuery
# @author: Heng Yu
'''

from socket import *
import time
import func


#rs server地址
rsAddr = ('127.0.0.1', 65423)

#从cookie.txt中读取cookie
with open("./cookie.txt", "r") as f:
    cookie = int(f.read())

# #创建peer2rs通信中的client套接字
clientSocket = socket(AF_INET, SOCK_STREAM)

# #连接到rs
clientSocket.connect(rsAddr)

#1. 发送request of PQuery给rs
request = "GET PQuery P2P-DI/1.0\r\nDate: %s\r\nOS: Mac OS\r\nCookie: %d\r\n\r\n" % (time.ctime(time.time()), cookie)
clientSocket.send(request.encode())

#2. 接收来自rs的包含active peer list的response，并存储到文件
response = clientSocket.recv(5096).decode()  #分配了5MB的buffer用于存放reponse的字节

#3. 关闭连接
clientSocket.close()

#4. 输出数据
activePeers = func.parse_response_for_aplist(response)   #拿到字符串
if activePeers: #有其他peer在线
    #输出到文件，文件名为peerlist.txt
    with open("./peerlist.txt", "w") as f:
        f.write(activePeers)
else:   #没有其他peer在线
    #打印提示信息
    with open("./peerlist.txt", "w") as f:  #打开文件写入空字符方便后续操作
        f.write("")
    print("Sorry, no other peers alive! Please try again later.")
