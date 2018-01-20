#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017-12-16
@author: Joy
'''
import os
import re
import urlparse
import pickle
from datetime import datetime, timedelta
from sqlite3 import Timestamp
import zlib

class DiskCache(object):
    '''
    classdocs
    '''
    def __init__(self, cache_dir = 'cache', max_length = 255, expires = timedelta(days = 30)):
        '''
        Constructor
        '''
        self.cache_dir = cache_dir
        self.max_length = max_length
        self.expires = expires
        
    def url_to_path(self, url):
        components = urlparse.urlsplit(url)
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)
    
    def __getitem__(self, url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                result, timestamp = pickle.load(zlib.decompress(fp.read()))
                if self.has_expired(timestamp):
                    raise KeyError(url + 'has expired')
                return result
                #return pickle.load(zlib.decompress(fp.read()))
                #return pickle.load(fp)
        else:
            raise KeyError(url + 'does not exist')
    
    def __setitem__(self, url, result):
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        timestamp = datetime.utcnow()
        data = pickle.dumps((result, timestamp))
        with open(path, 'wb') as fp:
            fp.write(zlib.compress(data))
            
    def has_expired(self, timestamp):
        return datetime.utcnow() > timestamp + self.expires