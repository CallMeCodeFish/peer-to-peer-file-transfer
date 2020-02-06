#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-24-19 10:24
# RFC_server.py
# theme: code for peer server.
# @author: Heng Yu
'''

from socket import *
import threading
import fcntl
import time
import func2

#服务器参数
port = func2.port
serverAddr = ("", port)
maxConnection = 5

#重置RFC_index.txt
with open("./RFC_index_local.txt", "r") as f:
    rfc_index_local = f.read()  #str

with open("./RFC_index.txt", "w") as f:
    f.write(rfc_index_local)

#TCP server套接字
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddr)
serverSocket.listen(maxConnection)
print("Peer server starts running.\nWaiting for peer clients...")


#函数定义
def serve_client(sock, addr):   #!!addr可以删除
    #1. 接受request，并转换成数组
    request = sock.recv(1024).decode()
    request_array = func2.parse_client_request(request)
    #[['GET', 'Register', 'P2P-DI/1.0'], {'Host': 'www.baidu.com', 'OS': 'Mac OS', 'Cookie': '1'}, 'this is the data']

    #2. 处理request
    if "RFC-Index" == request_array[0][1]:  #client要求得到RFC_index.txt中存放的内容
        with open("./RFC_index.txt", "r") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            response_body = f.read()    #string，有可能为空字符串
            response_in_str = func2.create_response_with_rfc_index(response_body)   #str
            response = response_in_str.encode() #bytes
    else:   #"RFC" == request_array[0][1]  client要求从该server上下载某个RFC文档 
        #拿到RFC文档编号
        rfc_no = request_array[0][2].lstrip("0")    #str
        file_path = "./RFCs/rfc%s.txt.pdf" % rfc_no
        with open(file_path, "rb") as f:
            response_body_bytes = f.read()  #bytes
        response = func2.create_response_with_rfc_doc(response_body_bytes)    #bytes
    sock.send(response)
    
    #3.关闭tcp连接
    sock.close()   


while True:
    clientSocket, clientAddress = serverSocket.accept()
    print("A peer client is coming.")

    clientThread = threading.Thread(target = serve_client, args = [clientSocket, clientAddress])
    clientThread.start()
