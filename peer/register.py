#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-23-19 10:16
# register.py
# theme: 连接到rs进行register并且拿到active peer list保存到本地
# @author: Heng Yu
'''

from socket import *
import time
import func
import func2


#rs server地址
rsAddr = ('127.0.0.1', 65423)

#p2p中作为server的port
port = func2.port

#从cookie.txt中读取cookie
try:
    with open("./cookie.txt", "r") as f:
        cookie = int(f.read())
except:
    cookie = 0

#创建peer2rs通信中的client套接字
clientSocket = socket(AF_INET, SOCK_STREAM)

#连接到rs
clientSocket.connect(rsAddr)

#0. 在发送request of register之前先打开服务器


#1. 发送request到rs进行register
if cookie == 0:    #没有cookie，在request body中发送port给rs
    request = "GET Register P2P-DI/1.0\r\nDate: %s\r\nOS: Mac OS\r\n\r\nPort: %d" % (time.ctime(time.time()), port)
else:   #有cookie则在header中发送cookie给rs
    request = "GET Register P2P-DI/1.0\r\nDate: %s\r\nOS: Mac OS\r\nCookie: %d\r\n\r\n" % (time.ctime(time.time()), cookie)
clientSocket.send(request.encode())

#2. 从rs收到第一个response，根据cookie的值确定行为
response = clientSocket.recv(1024).decode()
if cookie == 0:
    #解析Set-cookie的值并保存
    cookie = func.parse_response_for_cookie(response)
    with open("./cookie.txt", "w") as f:
        f.write(str(cookie))

#3. 关闭连接
clientSocket.close()
