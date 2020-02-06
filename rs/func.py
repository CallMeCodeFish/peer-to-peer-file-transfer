#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-22-19 11:48
# func.py
# theme: Definitions of functions 
# @author: Heng Yu
'''

import threading
import time
import activepeer


#############

#函数定义

def parse_client_request(req):
    #从request中分离出body
    [requestHeader, body] = req.split("\r\n\r\n")   #将request(string)分解为[requestHeader(string), body(string)]

    #从requestHeader中分离header
    array_requestLine_and_header = requestHeader.split("\r\n")  #将requestHeader(string)分解为[requestLine(string), header-1(string), header-2(string), ... , header-n(string)]

    #将requestLine分解成字符串列表
    array_requestLine = array_requestLine_and_header[0].split(" ")  #将"GET Register P2P-DI/1.0"分解为["GET", "Register", "P2P-DI/1.0"]

    #将header-i转换成hash
    hash_header = {}
    for i in range(1, len(array_requestLine_and_header)):
        array_header = array_requestLine_and_header[i].split(": ")
        k = array_header[0]
        v = array_header[1]
        hash_header[k] = v
        # print(hash_header)  输出: {"fieldname": "fieldvalue"}       
    #返回result列表
    return [array_requestLine, hash_header, body] #[['GET', 'Register', 'P2P-DI/1.0'], {'Host': 'www.baidu.com', 'OS': 'Mac OS', 'Cookie': '1'}, 'this is the data']


#解析client在body中提供的port
def parse_port(p_str):
    port = int(p_str.split(": ")[1])
    # print(port)
    return port


#生成字符串response
def create_response_with_cookie(ap):
    return "P2P-DI/1.0 200 OK\r\nDate: %s\r\nOS: Mac OS\r\nSet-cookie: %d\r\n\r\n" % (time.ctime(time.time()), ap.cookie)


def create_reponse_with_peer_list(c, pl):
    response_body = ""
    for ap in pl:
        if ap.isactive and c != ap:
            response_body += ap.hostname
            response_body += ":"
            response_body += str(ap.port)
            response_body += "\n"
    
    if len(response_body):  #200 OK
        return "P2P-DI/1.0 200 OK\r\nDate: %s\r\nOS: Mac OS\r\n\r\n%s" % (time.ctime(time.time()), response_body)
    else:   #404 NOT_FOUND
        return "P2P-DI/1.0 404 NOT_FOUND\r\nDate: %s\r\nOS: Mac OS\r\n\r\n" % time.ctime(time.time())


def create_response_without_body():
    return "P2P-DI/1.0 200 OK\r\nDate: %s\r\nOS: Mac OS\r\n\r\n" % time.ctime(time.time())




#测试:
if __name__ == '__main__':
    #测试函数 parse_client_request(req)
    # request = "GET Register P2P-DI/1.0\r\nHost: www.baidu.com\r\nOS: Mac OS\r\nCookie: 1\r\n\r\nthis is the data"
    # parseResult = parse_client_request(request)
    # print(parseResult)

    #测试函数: parse_port(p_str)
    # parse_port("port: 12000")

    #测试函数: create_response_with_cookie(ap)
    # host = "192.168.0.110"
    # port = 50000
    # ap1 = activepeer.ActivePeer(host, port)
    # print(create_response_with_cookie(ap1))
    
    # #测试函数: create_response_with_peer_list(pl)
    # host = "192.168.0.155"
    # port = "40000"
    # ap2 = activepeer.ActivePeer(host, port)
    # host = "192.168.0.222"
    # port = 60000
    # ap3 = activepeer.ActivePeer(host, port)
    # aplist = [ap1, ap2, ap3]
    # print(create_reponse_with_peer_list(aplist))

    #测试create_reponse_with_peer_list(c, pl)函数
    client = activepeer.ActivePeer("192.168.0.1", 60000)
    peers = [client]
    # client_prime = activepeer.ActivePeer("192.138.0.111", 5000)
    # peers = [client, client_prime]
    result = create_reponse_with_peer_list(client, peers)
    print(result)

    pass

    