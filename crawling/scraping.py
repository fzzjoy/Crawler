#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017-11-12

@author: Joy
'''
from crawling import download
import time
from crawling import crawl_link

FIELDS = ('area', 'population', 'iso', 'country', 'capital',
         'continent', 'tld', 'currency_code', 'currency_name', 
         'phone', 'postal_code_format', 'postal_code_regex', 
         'languages', 'neighbours'
         )

import re
def re_scraper(html):
    results = {}
    for field in FIELDS:
        searchResult = re.search('<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field, html)
        if searchResult is None:
            results[field] = None
            print "not find [%s] informations!" % field
        else:
            results[field] = searchResult.groups()[0]
#             print "%s: [%s]" % (field, results[field])
    return results
    

from bs4 import BeautifulSoup
def bs_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = {}
    for field in FIELDS:
        findResult = soup.find('table')
        if findResult is not None:
            findResult = findResult.find('tr', id = 'places_%s__row' % field)
            if findResult is not None:
                findResult = findResult.find('td', class_= 'w2p_fw')
                if findResult is not None:
                    results[field] = findResult.text
#                     print "%s: [%s]" % (field, results[field])
#     print results
    return results

import lxml.html
def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        selectResult = tree.cssselect('table > tr#places_%s__row > td.w2p_fw' % field)
        if selectResult is None:
            print "not find [%s] informations!" % field
        else:
            results[field] = selectResult[0].text_content()
    return results



def scrape_callback(url, html):
    if re.search('/view/', url):
        row = []
        tree = lxml.html.fromstring(html)
        for field in FIELDS:
            selectResult = tree.cssselect('table > tr#places_%s__row > td.w2p_fw' % field)
            if selectResult is None:
                print "not find [%s] informations!" % field
            else:
                row.append(selectResult[0].text_content())
        print url, row 

def test_performance():
    NUM_ITERATIONS = 1000
    html = download('http://example.webscraping.com/places/default/view/1')
    if html is None:
        exit(0)   
    for name, scraper in [('Regular expressions',re_scraper),
                          ('BeautifulSoup', bs_scraper),
                          ('Lxml', lxml_scraper)]:
        start = time.time()
        for i in range(NUM_ITERATIONS):
            if scraper == re_scraper:
                re.purge() # 清除缓存
            result = scraper(html)
            if (result['area'] != '647,500 square kilometres'):
                print "%s scraper html has error happend!"
        end = time.time()
        print '%s: %.2f seconds' %(name, end - start)

if __name__ == '__main__':
    crawl_link("http://example.webscraping.com", '(/places/default/view/)', scrape_callback = scrape_callback)
    print "Hello python"