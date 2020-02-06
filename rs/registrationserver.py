#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-22-19 10:25
# registrationserver.py
# Code of the realization of registration server
# @author: Heng Yu
'''

from socket import *
import threading
import time
import activepeer
import func

#用户列表和和列表线程锁
apList = []
threadLock_of_apList = threading.Lock()
#创建用户线程列表

#RS服务器参数
rsServerAddress = ('', 65423)   #RS地址
maxConnection = 5  #最大等待数量


#TCP主套接字
rsSocket = socket(AF_INET, SOCK_STREAM)   
rsSocket.bind(rsServerAddress)
rsSocket.listen(maxConnection)
print("Registration server starts running.\nWaiting for clients...")

#client服务函数定义
def serve_client(sock, addr):
    #1. 接受request，拿到目标objectiveClient对象
    #1.1  拿到request转化成数组
    request = sock.recv(1024).decode()
    request_array = func.parse_client_request(request)
    #[['GET', 'Register', 'P2P-DI/1.0'], {'Host': 'www.baidu.com', 'OS': 'Mac OS', 'Cookie': '1'}, 'this is the data']

    #1.2 如果没有Cookie证明是第一次注册，创建新的ActivePeer对象
    objectiveClient = None
    isNewClient = False
    if request_array[1].get("Cookie") ==  None: #首次注册的client
        print("新用户")
        isNewClient = True
        #1.2.1 解析request body中的port
        port = func.parse_port(request_array[2])
        objectiveClient = activepeer.ActivePeer(addr[0], port)
        #1.2.2 将newPeer添加到apList数组
        threadLock_of_apList.acquire()
        apList.append(objectiveClient)
        threadLock_of_apList.release()
        print("新用户register")
    else:   #已存在的client
        threadLock_of_apList.acquire()
        for ap in apList:
            if int(request_array[1].get("Cookie")) == ap.cookie:
                objectiveClient = ap
                #更新该client的host
                objectiveClient.hostname = addr[0]
                break
        threadLock_of_apList.release()
        print("老用户回归")

    #2. 处理request
    if "Register" == request_array[0][1]:   #GET Register
        if isNewClient == False: #老司机
            objectiveClient.register()
            print("老用户Register")
        newThread = threading.Thread(target = objectiveClient.ttl_decrement)
        newThread.start()
        if isNewClient == False:    #老司机
            response = func.create_response_without_body()
        else:   #新司机
            response = func.create_response_with_cookie(objectiveClient)
        sock.send(response.encode())
        print("针对Register发回response")
    elif "PQuery" == request_array[0][1]:   #GET PQuery
        objectiveClient.pquery()
        #将当前active的peer作为response发给client
        threadLock_of_apList.acquire()
        response = func.create_reponse_with_peer_list(objectiveClient, apList)
        threadLock_of_apList.release()
        sock.send(response.encode())
        print("针对PQuery发回response")
    elif "KeepAlive" == request_array[0][1]:    #GET KeepAlive
        #刷新登陆次数、登录时间、ttl置default
        objectiveClient.keep_alive()
        #发送response给client
        response = func.create_response_without_body()
        sock.send(response.encode())
        print("针对KeepAlive发回response")
    else:   #GET Leave
        activepeer.show_attributes_of_activepeer(objectiveClient)
        objectiveClient.leave()       
        activepeer.show_attributes_of_activepeer(objectiveClient)
        #发送response给client
        response = func.create_response_without_body()
        sock.send(response.encode())
        print("针对Leave发回response")
    sock.close()
    print("rs断开tcp")

while True:
    #TCP主线程
    rsClientSocket, clientAddress = rsSocket.accept() #rsClientSocket -- 与client通信套接字线程
    print("A client is coming.")

    #创建client线程处理p2p服务
    clientThread = threading.Thread(target = serve_client, args = [rsClientSocket, clientAddress])
    clientThread.start()    #并不需要等
