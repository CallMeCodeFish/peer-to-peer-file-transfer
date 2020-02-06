#!usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on Sep-24-19 22:52
# rfcindex.py
# theme: 
# @author: Heng Yu
'''

import threading
import time

class RFCIndex(object):

    ttl_default = 7200

    def __init__(self, n, title, host):
        self.number = n
        self.title = title
        self.host = host
        self.ttl = RFCIndex.ttl_default

        # self.__ttl_thread_lock = threading.Lock()
    

    def ttl_decrement(self):
        while 0 < self.ttl:
            time.sleep(1)
            self.ttl -= 1
