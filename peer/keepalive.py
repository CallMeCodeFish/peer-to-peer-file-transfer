#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-23-19 17:02
# keepalive.py
# theme: 连接到rs保持keep alive，刷新rs该client的状态
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


#创建peer2rs通信中的client套接字
clientSocket = socket(AF_INET, SOCK_STREAM)

#连接到rs
clientSocket.connect(rsAddr)

#1. 发送request到rs请求keep alive
request = "GET KeepAlive P2P-DI/1.0\r\nDate: %s\r\nOS: Mac OS\r\nCookie: %d\r\n\r\n" % (time.ctime(time.time()), cookie)
clientSocket.send(request.encode())

#2. 接收来自rs的response
response = clientSocket.recv(1024).decode()
#不需要对response进行解析和操作
# print(response)

#3. 关闭连接
clientSocket.close()