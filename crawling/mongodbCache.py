# -*- coding: utf-8 -*-
'''
Created on 2018-1-3

@author: Joy
'''

# rom pymongo import MongoClient
from datetime import timedelta
from datetime import datetime
import time
from pymongo import *

class MongoCache:
    def __init__(self, client = None, expires = timedelta(days = 30)):
        #如果入参client为空，则self.client = MongoClient(...)，否则self.client 等于入参的client
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db = self.client.cache
#         self.db.webpage.create_index([("time", ASCENDING)], expireAfterSeconds = expires.total_seconds())
        self.db.webpage.ensure_index("date", expireAfterSeconds=3000*60) 

    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return record['result']
        else:
            raise KeyError(url + 'does not exist')
    
    def __setitem__(self, url, result):
        record = {'result': result, 'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert = True)
        
        

if __name__ == '__main__':
    cache = MongoCache()
    result = {'html': '123'}
    url = 'www.baidu.com'
    cache[url] = result;
    print cache[url]
#     time.sleep(60)
#     try:
#         cache[url]
#     except Exception as e:
#         print 'cache[url] error:', str(e)  
    print "Hello python"