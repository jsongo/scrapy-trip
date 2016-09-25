#!/usr/bin/env python
# coding=utf-8
from scrapy.crawler import CrawlerProcess
# from scrapy import log
import logging
import os

from pymongo import MongoClient

from trip.spiders.breadProduct import BreadProductSpider
from scrapy.utils.project import get_project_settings

log = logging.getLogger()

urlToCrawl = "http://api.breadtrip.com/hunter/products/v2/?city_name=%s&sorted_id=1&start=0"

if __name__ == "__main__":
    conn = MongoClient('127.0.0.1', 27018)
    db = conn['clover']

    cities = db.city.find({"$or": [{"prodCrawled": {"$exists": False}}, {"prodCrawled": False}]})
    urls = []
    # cnt = 10 
    for city in cities:
        # log.debug(city)
        url = urlToCrawl%city['nameCn'].encode('utf-8')
        # urls.append({'id': city['id'], 'url': url})
        os.popen('python runBreadProduct.py "%s" %s' % (url, city['id'].encode('utf-8')))
        # cnt -= 1
        # if cnt <= 0:
            # break

    process = CrawlerProcess(get_project_settings())
    process.crawl(BreadProductSpider, urls=urls)
    process.start()
