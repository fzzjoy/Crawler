#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017-11-11

@author: Joy
'''
import datetime
import time
from future.backports.urllib.parse import urlparse

class Throttle(object):
    '''
    classdocs
    '''

    # 单位秒
    def __init__(self, delay):
        '''
        Constructor
        '''
        self.delay = delay 
        self.domains = {}
        
    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()