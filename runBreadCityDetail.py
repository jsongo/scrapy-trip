#!/usr/bin/env python
# coding=utf-8
from scrapy.crawler import CrawlerProcess
# from scrapy.crawler import CrawlerRunner
from scrapy import log

from pymongo import MongoClient

from trip.spiders.breadCityDetail import BreadCityDetailSpider
from scrapy.utils.project import get_project_settings
# from twisted.internet import reactor

if __name__ == "__main__":
    conn = MongoClient('127.0.0.1', 27018)
    db = conn['clover']

    cities = db.city.find({})
    urls = []
    # cnt = 2
    for city in cities:
        log.msg(city, level=log.INFO)
        urls.append({'id': city['id'], 'url': city['url']})
        # if cnt <= 0:
            # break
        # cnt -= 1

    process = CrawlerProcess(get_project_settings())
    process.crawl(BreadCityDetailSpider, urls=urls)
    process.start()

    # runner = CrawlerRunner(get_project_settings())
    # d = runner.crawl(BreadCityDetailSpider, urls=urls, cities=cities)
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run()
