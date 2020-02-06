#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-24-19 16:19
# func2.py
# theme: functions that will be used for a peer server to communicate with peer clients.
# @author: Heng Yu
'''

from socket import *
import threading
import fcntl
import time


#global variable
port = 65402



#读取RFC_index.txt的内容，返回list。注意可能为空
# def get_rfc_index():
#     with open("./RFC_index.txt", "r") as f:
#         fcntl.flock(f.fileno(), fcntl.LOCK_EX)
#         result = f.readlines()
#     return result


#解析收到的request成数组
def parse_client_request(req):
    [requestHeader, body] = req.split("\r\n\r\n")
    #[requestHeader(string), body(string)]

    array_requestLine_and_header = requestHeader.split("\r\n")
    #[requestLine(string), header-1(string), header-2(string), ... , header-n(string)]

    array_requestLine = array_requestLine_and_header[0].split(" ")
    #["GET", "Register", "P2P-DI/1.0"]

    hash_header = {}
    for i in range(1, len(array_requestLine_and_header)):
        array_header = array_requestLine_and_header[i].split(": ")
        k = array_header[0]
        v = array_header[1]
        hash_header[k] = v
    #{'Host': 'www.baidu.com', 'OS': 'Mac OS', 'Cookie': '1'}

    return [array_requestLine, hash_header, body]
#[['GET', 'Register', 'P2P-DI/1.0'], {'Host': 'www.baidu.com', 'OS': 'Mac OS', 'Cookie': '1'}, 'this is the data']


#为RFC-Index生成response，返回str
def create_response_with_rfc_index(rb):
    if len(rb) == 0:    #该RFC_index.txt文件为空，发送404 NOT FOUND
        code = 404
        phrase = "NOT FOUND"
    else:   #不为空 发送200 OK
        code = 200
        phrase = "OK"
    response = "P2P-DI/1.0 %d %s\r\nDate: %s\r\nOS: Mac OS\r\n\r\n%s" % (code, phrase, time.ctime(time.time()), rb)
    return response


#为RFC xxxx生成response, 返回bytes
def create_response_with_rfc_doc(rb):
    code = 200
    phrase = "NOT FOUND"
    response_without_body = "P2P-DI/1.0 %d %s\r\nDate: %s\r\nOS: Mac OS\r\n\r\n" % (code, phrase, time.ctime(time.time()))
    response_in_bytes = response_without_body.encode() + rb
    return response_in_bytes




if __name__ == "__main__":
    pass

    #测试get_rfc_index()
    # print("打印函数返回值")
    # result = get_rfc_index()
    # print(result)
    # print("打印返回的数组长度")
    # print(len(result))
    # if len(result):
    #     print("True")
    # else:
    #     print("False")
    # print("打印完成")

    #测试create_response_with_rfc_index(rb)
    # with open("./RFC_Index.txt", "r") as f:
    #     response_body = f.read()
    # response = create_response_with_rfc_index(response_body)
    # print(response)

    # print(int("0042".lstrip("0")) + 10)

    # str1 = "Hello, "
    # str2 = "world"
    # b1 = str1.encode()
    # b2 = str2.encode()
    # b = b1 + b2

    # print(b1)
    # print(b)
    # print(b.decode())

    #测试函数create_response_with_rfc_doc(rb)
    # with open("./Rezume_Heng Yu.pdf", "rb") as f:
    #     contents = f.read() #bytes
    
    # response = create_response_with_rfc_doc(contents)   #bytes
    # header, body = response.split("\r\n\r\n".encode())
    # print(header.decode())
    # with open("./oooook.pdf", "wb") as f:
    #     f.write(body)

    



