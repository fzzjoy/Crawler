#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017-12-16

@author: Joy
'''
from downloader import Downloader
import re
import urlparse
from diskCache import DiskCache
from mongodbCache import MongoCache

def crawl_link(seed_url, link_regex = None, user_agent = 'wswp', max_urls = -1, delay = 5, proxies = None, max_depth = 2, num_retries = 1, scrape_callback = None, cache = None):
    crawl_queue = [seed_url]
    seen = {seed_url: 0}
    num_urls = 0
    D = Downloader(delay = delay, user_agent=user_agent, cache=cache)
    
    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        html = D(url) #调用_call_方法
        if html is None:
            print url + " is none"
            return
        
        links = []
        if scrape_callback:
            links.extend(scrape_callback(url, html) or []) #or []:代表追加的是个空列表
        # check is max depth
        depth = seen[url]
        if depth != max_depth:
            for link in get_links(html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)
                    # check the has down
                    if link not in seen:
                        seen[link] = depth + 1
                        crawl_queue.append(link)
                        
def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

if __name__ == '__main__':
    crawl_link(seed_url="http://example.webscraping.com", link_regex='(/places/default/view/)',  cache=MongoCache())
    print 'Hello python'
    pass
