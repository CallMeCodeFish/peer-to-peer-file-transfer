#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-23-19 15:16
# func.py
# theme: functions that will be used for a client to communicate with rs server.
# @author: Heng Yu
'''

import time

#从response中解析出Set-cookie的值
def parse_response_for_cookie(r):
    response_array = parse_response_to_array(r)
    return int(response_array[1]["Set-cookie"])


#将response处理成array对象
def parse_response_to_array(r):
    [responseHeader, body] = r.split("\r\n\r\n")
    array_responseLine_and_header = responseHeader.split("\r\n")
    array_responseLine = array_responseLine_and_header[0].split(" ")

    hash_header = {}
    for i in range(1, len(array_responseLine_and_header)):
        array_header = array_responseLine_and_header[i].split(": ")
        k = array_header[0]
        v = array_header[1]
        hash_header[k] = v
    
    return [array_responseLine, hash_header, body]


#从response中解析出active peer list
def parse_response_for_aplist(r):
    response_array = parse_response_to_array(r)
    if response_array[0][1] == "404":
        return False
    else:
        return response_array[2]



if __name__ == "__main__":
    #测试parse_response_for_cookie(r)
    # response = "P2P-DI/1.0 200 OK\r\nDate: %s\r\nOS: Mac OS\r\nSet-cookie: %d\r\n\r\n" % (time.ctime(time.time()), 9527)
    # print (parse_response_for_cookie(response) + 100)

    #测试parse_response_for_aplist(r)
    # response = "P2P-DI/1.0 404 OK\r\nDate: %s\r\nOS: Mac OS\r\n\r\n2131" % time.ctime(time.time())
    # if response:        
    #     print(parse_response_for_aplist(response))
    # else:
    #     print("False")

    #测试parse_response_to_array(r)
    # response = "P2P-DI/1.0 200 OK\r\nDate: %s\r\nOS: Mac OS\r\n\r\n" % time.ctime(time.time())
    # result = parse_response_to_array(response)
    # print(result)
    pass