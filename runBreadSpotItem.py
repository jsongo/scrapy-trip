#!/usr/bin/env python
# coding=utf-8

import sys
from scrapy.crawler import CrawlerProcess
from scrapy import log
from scrapy.utils.project import get_project_settings

from trip.spiders.breadSpots import BreadSpotsSpider

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())

    process.crawl(BreadSpotsSpider, spiderUrl=sys.argv[1], cityId=sys.argv[2])
    process.start()
