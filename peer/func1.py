#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-24-19 18:33
# func1.py
# theme: 
# @author: Heng Yu
'''

import time


#得到active peer list，返回类型: list
def parse_for_active_peer_list(ap):
    ap = ap.rstrip()    #remove '\n' at the end of the string
    ap_string_list = ap.split("\n")
    #['192.168.0.101:1111', '192.168.0.102:2222', '192.168.0.103:3333', '192.168.0.104:4444']
    ap_list = []
    for ap in ap_string_list:
        host, port = ap.split(":")
        # print((host, int(port)))
        ap_list.append((host, int(port)))

    return ap_list  #[('192.168.0.101', 1111), ('192.168.0.102', 2222), ('192.168.0.103', 3333), ('192.168.0.104', 4444)]


#解析来自peer server的response
def parse_response_for_list(r):
    responseHeader, body = r.split("\r\n\r\n")
    header_list = responseHeader.split("\r\n")
    #['P2P-DI/1.0 200 OK', 'Date: Tue Sep 24 19:09:56 2019', 'OS: Mac OS']

    response_line_list = header_list[0].split(" ")
    #['P2P-DI/1.0', '200', 'OK']  or  ['P2P-DI/1.0', '404', 'NOT', 'FOUND']

    headers = {}
    for i in range(1, len(header_list)):
        k, v = header_list[i].split(": ")
        headers[k] = v
    #{'Date': 'Tue Sep 24 19:17:55 2019', 'OS': 'Mac OS'}
    return [response_line_list, headers, body]  #[['P2P-DI/1.0', '200', 'OK'], {'Date': 'Tue Sep 24 19:20:23 2019', 'OS': 'Mac OS'}, ''] or [['P2P-DI/1.0', '404', 'NOT', 'FOUND'], {'Date': 'Tue Sep 24 19:19:20 2019', 'OS': 'Mac OS'}, '']


#将body中rfc_index字符串解析为列表
def parse_body_for_index_list(s, ap):
    source_host_name = ap[0] + ":" + str(ap[1])
    s_rstrip = s.rstrip()   #remove '\n' at the end of string s
    record_string_list = s_rstrip.split("\n")
    record_list = []
    for rs in record_string_list:
        record = rs.split("  ")
        if len(record) == 2:
            record.append(source_host_name)
        record_list.append([int(record[0]), record[1], record[2]])
    return record_list  #[[42, 'file-42', '192.168.0.101:80'], [432, 'file-432', '192.168.0.102:80'], [142, 'file-142', '192.168.0.103:80'], [556, 'file-556', '192.168.0.104:80'], [465, 'file-465', '192.168.0.105:80']]

#将解析后的rfc_index_list转换成字符串
def create_index_string_to_merge(il):
    temp_list = []
    for i in il:
        index_string = "%d  %s  %s" % (i[0], i[1], i[2])
        temp_list.append(index_string)
    return "\n".join(temp_list) + "\n"

#seek record from merged RFC index list and return the host owning the record
def seek_record_from_merged_index(n, l):
    for e in l:
        if n == e.number and 0 < e.ttl:
            return e
    return False


#parse string for host tuple: (host, port)
def parse_for_objective_server(p):
    r = p.host
    host, port = r.split(":")
    return (host, int(port))


if __name__ == "__main__":
    pass

    #测试函数parse_for_active_peer_list(ap)
    # activepeers = "192.168.0.101:1111\n192.168.0.102:2222\n192.168.0.103:3333\n192.168.0.104:4444\n"
    # print(parse_for_active_peer_list(activepeers))

    #测试函数parse_response_for_list(r)
    # code = 200
    # # code = 404
    # phrase = "OK"
    # # phrase = "NOT FOUND"
    # rb = ""
    # response = "P2P-DI/1.0 %d %s\r\nDate: %s\r\nOS: Mac OS\r\n\r\n%s" % (code, phrase, time.ctime(time.time()), rb)
    # print(parse_response_for_list(response))

    #测试函数parse_body_for_index_list(s)

    # ap = ("127.0.0.1", 50000)
    # body = "42 file-42\n432 file-432 192.168.0.102:80\n142 file-142\n556 file-556 192.168.0.104:80\n465 file-465 192.168.0.105:80\n"

    # print(parse_body_for_index_list(body, ap))

    #测试函数create_index_string_to_merge(il)
    # il = parse_body_for_index_list(body, ap)
    # print(create_index_string_to_merge(il))
