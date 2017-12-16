#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017-11-5

@author: Joy
'''

import itertools
import urllib2
import re
import urlparse
import robotparser
from throttle import Throttle
from distutils.filelist import findall
import _threading_local
import lxml.html

rp = robotparser.RobotFileParser()

def Olddownload(url, user_agent = 'wswp', num_retries = 2):
    print 'Downloading ', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        htmlfile = urllib2.urlopen(request, timeout = 10) 
        html = htmlfile.read()
    except Exception as e:
        print 'Download error:', str(e)
        html = None
        if num_retries > 0:
            # 当下载遇到5xx错误码时，尝试重新下载
            if hasattr(e, 'code') and 500 <= e.code <= 600:
                return download(url, num_retries - 1)
    return html

def download(url, user_agent = 'wswp', proxy = None, num_retries = 2):
    print 'Downloading ', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
#         htmlfile = urllib2.urlopen(request, timeout = 10)
        htmlfile = opener.open(request, timeout = 15) 
        html = htmlfile.read()
    except Exception as e:
        print 'Download error:', str(e)
        html = None
        if num_retries > 0:
            # 当下载遇到5xx错误码时，尝试重新下载
            if hasattr(e, 'code') and 500 <= e.code <= 600:
                return download(url, user_agent, proxy, num_retries - 1)
    return html

# 网站地图爬取
def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    if sitemap is None:
        print 'Download error ', url
        return None
    links = re.findall('href="(.*?)"', sitemap)
    print len(links)
    for link in links:
        html = download("http://example.webscraping.com" + link)
  
# 数据库ID遍历爬虫
def crawl_byID(oriUrl):
    max_errors = 5
    num_errors = 0
    for page in itertools.count(1):
        url = oriUrl + "%d"  %page
        html = download(url)
        if html is None:
            print "download fail " + url  
            num_errors += 1
            if num_errors == max_errors:
                break
        else:
            num_errors = 0
            print "download success " + url    
   
# 链接爬虫
def crawl_link(seed_url, link_regex, max_depth = 2, delay = 3, scrape_callback = None):
    crawl_queue = [seed_url]
    seen = {seed_url: 0}
    throttle = Throttle(delay)
    while crawl_queue:
        url = crawl_queue.pop()
        throttle.wait(url)
        html = download(url)
        if html is None:
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
#     crawl_sitemap('http://example.webscraping.com/sitemap.xml')
#     crawl_byID("http://example.webscraping.com/places/default/view/")
    crawl_link("http://example.webscraping.com", '(/places/default/view/)')
    print 'Hello python'
    pass