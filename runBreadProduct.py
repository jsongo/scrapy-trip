#!/usr/bin/env python
# coding=utf-8

import sys
from scrapy.crawler import CrawlerProcess
# from scrapy import log
import logging
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

from trip.spiders.breadProduct import BreadProductSpider
from trip.spiders.breadProductPage import BreadProductPageSpider

log = logging.getLogger()
min = 8570 # 9801
max = 16874 # 14992
# 15973

if __name__ == "__main__":
    conn = MongoClient('127.0.0.1', 27018)
    db = conn['clover']

    process = CrawlerProcess(get_project_settings())

    data = sys.argv[1]
    if data == 'all':
        urls = []
        # cnt = 3
        for id in xrange(min, max):
            url = 'http://web.breadtrip.com/hunter/product/%d' % id
            d = db.product.find({'id': id, 'likes': {'$exists': False}})
            # log.debug(d)
            exists = True if d.count() else False
            urls.append({'url': url, 'pid': id, 'exists': exists})
            # cnt -= 1
            # if cnt < 0:
                # break
        process.crawl(BreadProductPageSpider, urls=urls)
    else:
        process.crawl(BreadProductSpider, spiderUrl=data, cityId=sys.argv[2])
    process.start()
