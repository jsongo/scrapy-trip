#!/usr/bin/env python
# coding=utf-8
from scrapy.crawler import CrawlerProcess
# from scrapy.crawler import CrawlerRunner
import logging

from pymongo import MongoClient

from trip.spiders.breadGuide import BreadGuideSpider
from scrapy.utils.project import get_project_settings

log = logging.getLogger()

if __name__ == "__main__":
    conn = MongoClient('127.0.0.1', 27018)
    db = conn['clover']

    guides = db.guide.find({}) # 'intro': {'$exists': False}}) 
    log.debug('==>>%d' % guides.count())
    urls = []
    # cnt = 2
    for guide in guides:
        # log.msg(guide, level=log.INFO)
        log.debug(guide)
        urls.append({'id': guide['id']})
        # break
        # cnt -= 1
        # if cnt <= 0:
            # break

    process = CrawlerProcess(get_project_settings())
    process.crawl(BreadGuideSpider, urls=urls)
    process.start()

    # runner = CrawlerRunner(get_project_settings())
    # d = runner.crawl(BreadCityDetailSpider, urls=urls, cities=cities)
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run()
