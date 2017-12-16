#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017-12-16

@author: Joy
'''
from throttle import Throttle
from random import random
import urllib2
import urlparse

class Downloader(object):
    '''
    classdocs
    '''


    def __init__(self, delay = 5, user_agent = 'wswp',
                 proxies = None, num_retries = 1, cache = None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache
        self.opener = None
        '''
        Constructor
        '''
    #当调用实例名时便会调用该方法
    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                print url + " is not available in cache!"
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    result = None
                else:
                    print url + " is available in cache!"
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries)
            if self.cache and result is not None:
                self.cache[url] = result;
            else:
                return None
        return result['html']    
                        
    def download(self, url, headers, proxy, num_retries, data = None):
        print 'Downloading ', url
        # python中的逻辑运算和普通的不一样
        request = urllib2.Request(url, data, headers or {})
        opener = self.opener or urllib2.build_opener()
        code = 200
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
    #         htmlfile = urllib2.urlopen(request, timeout = 10)
            # timeout： s（秒）
            htmlfile = opener.open(request, timeout = 15) 
            html = htmlfile.read()
        except Exception as e:
            print 'Download error:', str(e)
            html = None
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= e.code <= 600:
                    # 当下载遇到5xx错误码时，尝试重新下载
                    return self.download(url, headers, proxy, num_retries - 1, data)
                else:
                    return None
            else:
                return None
        return {'html':html, 'code':code}
    
