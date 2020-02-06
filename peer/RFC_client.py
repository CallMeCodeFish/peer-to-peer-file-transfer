#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-24-19 18:03
# RFC_client.py
# theme: code for peer client
# @author: Heng Yu
'''

from socket import *
import threading
import fcntl
import time
import func1
import rfcindex

# #localhost ip
# serverport = 65400
# hostname = gethostbyname(gethostname())
# ip = (hostname, serverport)

#要下载的rfc文档的no
rfc_no = 42

#initialize a flag indication whether the document desired is downloaded at last
is_downloaded = False

#RFCIndex类对象的list
rfc_from_servers = []
# thread_lock_for_rfc_list = threading.Lock()

#拿到peer server的信息
with open("./peerlist.txt", "r") as f:
    activepeers = f.read()  #str
if len(activepeers) == 0:   #当前没有其他活跃用户
    print("No active peers in P2P system now.\n Please run \"pquery.py\" a few moments later.")
else:   #有活跃用户
    apList = func1.parse_for_active_peer_list(activepeers)

    #TCP client套接字
    clientSocket = socket(AF_INET, SOCK_STREAM)

    for ap in apList:
        try:
            clientSocket.connect(ap)    #!!有可能连不上，需要处理异常
        except ConnectionRefusedError:
            continue

        #1. 向peer server发送request: GET RFC-Index
        request = "GET RFC-Index P2P-DI/1.0\r\nDate: %s\r\nOS: Mac OS\r\n\r\n" % time.ctime(time.time())
        clientSocket.send(request.encode())

        #2. 拿到并解析来自peer server的response
        response = clientSocket.recv(1024).decode()
        response_list = func1.parse_response_for_list(response)

        #3. 关闭tcp连接
        clientSocket.close()

        #4. 处理本地的RFC_index.txt文件
        if "200" == response_list[0][1]:    #需要进行merge
            body = response_list[2]    #str
            rfc_index_list = func1.parse_body_for_index_list(body, ap)

            #merge
            new_index_to_merge = func1.create_index_string_to_merge(rfc_index_list)
            with open("./RFC_index.txt", "a") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                f.write(new_index_to_merge)

            #创建RFCIndex类对象，对ttl进行倒计时
            for e in rfc_index_list:
                record = rfcindex.RFCIndex(e[0], e[1], e[2])    #Instance of RFCIndex Class
                record_thread = threading.Thread(target = record.ttl_decrement)
                record_thread.start()
                rfc_from_servers.append(record)

            #Find the desired document in merged RFC index
            desired_record = func1.seek_record_from_merged_index(rfc_no, rfc_from_servers)  #Instance of RFCIndex Class, or False

            if desired_record:
                objective_server = func1.parse_for_objective_server(desired_record)

                #5. tcp连接到目标server
                clientSocket = socket(AF_INET, SOCK_STREAM)
                try:
                    clientSocket.connect(objective_server)  #!!可能连不上
                except ConnectionRefusedError:
                    continue

                #5.1 发出RFC request请求
                request = "GET RFC %d P2P-DI/1.0\r\nDate: %s\r\nOS: Mac OS\r\n\r\n" % (rfc_no, time.ctime(time.time()))
                clientSocket.send(request.encode())

                #5.2 接收response
                response = clientSocket.recv(1024)  #bytes

                #5.3 关闭连接
                clientSocket.close()

                #5.4 保存文件和index记录
                is_downloaded = True

                response_header, response_body = response.split("\r\n\r\n".encode())
                #保存RFC文档
                with open("./RFCs/rfc%d.txt.pdf" % rfc_no, "wb") as f:
                    f.write(response_body)

                #在local index中添加记录
                new_index_record = "%d %s\n" % (rfc_no, desired_record.title)
                with open("./RFC_index_local.txt", "a") as f:
                    f.write(new_index_record)

                #在merged文档中添加记录
                with open("./RFC_index.txt", "a") as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    f.write(new_index_record)
                
                #5.5 退出进程
                break

#6. 终止ttl倒计时线程
for e in rfc_from_servers:
    e.ttl = 0
                
#7. 打印提示信息
if is_downloaded:   #obtained the desired document
    print("Document downloaded successfully!")
else:
    print("Sorry, document is not found.")
