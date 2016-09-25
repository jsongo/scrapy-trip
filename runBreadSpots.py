#!/usr/bin/env python
# coding=utf-8
from scrapy.crawler import CrawlerProcess
# from scrapy import log
import logging

from pymongo import MongoClient

from trip.spiders.breadSpots import BreadSpotsSpider
from scrapy.utils.project import get_project_settings

log = logging.getLogger()

if __name__ == "__main__":
    conn = MongoClient('127.0.0.1', 27018)
    db = conn['clover']

    cities = db.city.find({"$or": [{"crawled": {"$exists": False}}, {"crawled": False}]})
    urls = []
    # cnt = 100
    for city in cities:
        # if city.has_key('crawled') and city['crawled']:
            # continue
        # log.msg(city, level=log.INFO)
        log.debug(city)
        urls.append({'id': city['id'], 'url': city['url'] + 'sight/more?next_start=0'})
        # log.debug('.......new city scraping...... %s ' % urls[len(urls)-1])
        # cnt -= 1
        # if cnt <= 0:
            # break

    process = CrawlerProcess(get_project_settings())
    process.crawl(BreadSpotsSpider, urls=urls)
    process.start()
